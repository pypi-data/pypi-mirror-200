import copy
import json
import os
import webbrowser
from dataclasses import dataclass, asdict
from multiprocessing.pool import ThreadPool
from typing import Optional, List

import tqdm

import mstuff
import oexp.gen as gen

from mstuff.http import API, Login

_api = API(gen.ONLINE_EXP_HEROKU_HOST)

_enable_progress_bars = True


def _enable_local_mode():
    global _api
    _api._url_prefix = gen.LOCAL_HOST


def _enable_stage_mode(token: str):
    global _api
    _api._url_prefix = "https://oexp-staging.herokuapp.com/"
    _api._auth_tokens["stagingAuth"] = token


mstuff.warn_if_old("oexp")


def login(username, password):
    return OnlineExperiments(username, password)


@dataclass
class OnlineExperiments(Login):
    username: str
    password: str

    def __repr__(self):
        return f"oexp Login (username={self.username})"

    @property
    def prolific_key(self):
        raise ("you cannot see the prolific key, you can only replace it.")

    @prolific_key.setter
    def prolific_key(self, value):
        if not isinstance(value, str):
            raise ("prolific key must be a string")
        _api.http_put("/prolific-key", data=value, login=self)

    def list_experiments(self):
        return [self._live_experiment(e.uid) for e in self._list_experiment_data()]

    def experiment(self, name):
        exps = self._list_experiment_data()
        for e in exps:
            if e.name == name:
                return self._live_experiment(e.uid)
        resp = _api.http_post("/experiments", login=self)
        exp = json.loads(resp.text)
        exp = mstuff.class_from_args(ExperimentData, exp)
        exp = self._live_experiment(exp.uid)
        exp.name = name
        return exp

    def _list_experiment_data(self):
        resp = _api.http_get("/experiments", login=self)
        exps = json.loads(resp.text)
        return [mstuff.class_from_args(ExperimentData, e) for e in exps]

    def _experiment_data_by_id(self, uid):
        exps = self._list_experiment_data()
        for e in exps:
            if e.uid == uid:
                return e
        raise Exception(f"could not find experiment with uid {uid} in [{[e.uid for e in exps]}]")

    def _live_experiment(self, uid):
        return Experiment(self, uid)


@dataclass
class Trial:
    query: str
    distractors: List[str]


@dataclass
class TrialManifest:
    trials: List[Trial]
    skip: bool = False


@dataclass
class ExperimentData:
    uid: int
    name: str
    manifests: Optional[List[TrialManifest]] = None
    prolificStudyID: Optional[str] = None
    css: Optional[str] = None


class _CommonQueryParams:
    expUID = "experimentUID"


@dataclass
class Experiment:
    user: OnlineExperiments
    uid: int

    @property
    def name(self):
        return self.user._experiment_data_by_id(self.uid).name

    @name.setter
    def name(self, value):
        update = self.user._experiment_data_by_id(self.uid)
        update.name = value
        _api.http_put("/experiments", json=asdict(update), login=self.user)

    @property
    def manifests(self):
        return self.user._experiment_data_by_id(self.uid).manifests

    @manifests.setter
    def manifests(self, value):
        safe_value = copy.deepcopy(value)
        update = self.user._experiment_data_by_id(self.uid)
        if not isinstance(safe_value, list):
            raise Exception("trials must be a list")
        for v in safe_value:
            if not isinstance(v, TrialManifest):
                raise Exception(f"trials must be a list of {TrialManifest}")
            for t in v.trials:
                if not isinstance(t, Trial):
                    raise Exception(f"trials must be a list of lists of {Trial}")
                if len(t.distractors) != 5:
                    raise Exception("there must be 5 distractors per trial")
        update.manifests = safe_value
        _api.http_put("/experiments", json=asdict(update), login=self.user)

    @property
    def css(self):
        return self.user._experiment_data_by_id(self.uid).css

    @css.setter
    def css(self, value):
        if not isinstance(value, str):
            raise Exception("css must be a string")
        update = self.user._experiment_data_by_id(self.uid)
        update.css = value
        _api.http_put("/experiments", json=asdict(update), login=self.user)

    def delete(self):
        _api.http_delete("/experiments", json=asdict(self.user._experiment_data_by_id(self.uid)), login=self.user)

    def open(self):
        webbrowser.open_new_tab(
            _api._url_prefix + f"/newform/{self.uid}?prolificPID=test-{self.user.username}&sessionID=test-session-{self.user.username}"
        )

    def subject_data(self):
        resp = _api.http_get(gen.DOWNLOAD_SUBJECT_DATA_V2_PATH, login=self.user,
                             params={_CommonQueryParams.expUID: str(self.uid)})
        json_txt = resp.text
        return json.loads(json_txt)

    def link_prolific(self, prolific_study_id):
        resp = _api.http_get(gen.LINK_PROLIFIC_PATH, login=self.user,
                             params={
                                 _CommonQueryParams.expUID: str(self.uid),
                                 "prolificStudyID": prolific_study_id
                             })
        return json.loads(resp.text)

    def delete_all_images(self):
        _api.http_delete(
            gen.IMAGES_PATH.replace("{experimentUID}", str(self.uid)),
            login=self.user,
        )

    def _get_images_to_send(self, root_dir):
        reqs = {}
        for root, subdirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    with open(os.path.join(root, file), "rb") as f:
                        space_file_relpath = os.path.join(os.path.relpath(root, root_dir), file)
                        reqs[space_file_relpath] = dict(
                            path=gen.IMAGES_PATH.replace("{experimentUID}", str(self.uid)) + "/" + space_file_relpath,
                            login=self.user,
                            data=f.read()
                        )
        return reqs

    # def upload_images(self, root_dir):
    #
    #     images_to_send = self._get_images_to_send(root_dir)
    #
    #     # https://stackoverflow.com/questions/2212643/python-recursive-folder-read
    #     pool = ThreadPool(processes=100)
    #     def task(im):
    #         _api.http_put(**im)
    #
    #     with pool:
    #         if _enable_progress_bars:
    #             tqdm.tqdm(pool.map(task, images_to_send.values()))
    #         else:
    #             pool.map(task, images_to_send.values())
    #     return list(images_to_send.keys())

    # https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp
    def upload_images(self, root_dir):
        images_to_send = self._get_images_to_send(root_dir)
        for req in images_to_send.values():
            req["method"] = "put"
        _api.async_requests(images_to_send.values())
        return list(images_to_send.keys())

    def list_images(self):
        resp = _api.http_get(
            gen.IMAGES_PATH.replace("{experimentUID}", str(self.uid)),
            login=self.user,
        )
        return json.loads(resp.text)

    def view_image(self, path):
        resp = _api.http_get(
            gen.IMAGE_VIEW_PATH.replace("{experimentUID}", str(self.uid)) + "/" + path,
            login=self.user,
        )
        temp_url = resp.text
        webbrowser.open_new_tab(temp_url)
        return temp_url
