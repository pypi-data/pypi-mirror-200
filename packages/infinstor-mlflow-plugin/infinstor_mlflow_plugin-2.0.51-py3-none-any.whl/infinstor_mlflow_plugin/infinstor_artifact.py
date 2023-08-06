import pathlib
import posixpath
from typing import List, Tuple, Union
from infinstor_mlflow_plugin.tokenfile import get_token, get_id_token
from .utils import set_builtins_with_serverside_config
from infinstor_mlflow_plugin import login
from mlflow.store.artifact.s3_artifact_repo import S3ArtifactRepository
import os
import builtins
from urllib.parse import quote
from urllib.request import unquote, urlretrieve
from requests.exceptions import HTTPError
import requests
import mlflow
from mlflow.utils.file_utils import relative_path_to_artifact_path
from mlflow.entities import FileInfo
import xml.etree.ElementTree as ET
import xml.etree.ElementTree 
from mlflow import data
from mlflow.exceptions import MlflowException
from . import tokenfile

import logging
from .utils import _get_logger
logger:logging.Logger = _get_logger(__name__)

class InfinStorArtifactRepository(S3ArtifactRepository):
    """LocalArtifactRepository provided through plugin system"""
    is_plugin = True

    def __init__(self, artifact_uri:str):
        """
        _summary_

        Args:
            artifact_uri (str): This will not always be the run's artifact root URI (s3://<bucket_name>/path/to/run_id).  It can also be some path under the run's artifact root URI: similar to s3://<bucket_name>/path/to/run_id/path/to/subdir.  here run's artifact root URI is s3://<bucket_name>/path/to/run_id. For an example of the latter, see mlflow.git/tests/models/test_model.py(243)test_model_load_input_example_numpy().  Also the recipe.train() step of mlflow-recipe-examples/regression

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        #######
        # for log_artifact() or log_artifacts() call, we do not need to check if logging is happening under a 'deleted experiments', since log_artifact() and log_artifacts() need an active run and creating this run will fail under a deleted experiment
        #######
        self.srvc = login.bootstrap_from_mlflow_rest() 
        set_builtins_with_serverside_config(self.srvc)
        id_token, service = get_id_token(self.srvc['region'])
        rj = login.get_customer_info_rest(id_token)
        if 'usePresignedUrlForMLflow' in rj and rj['usePresignedUrlForMLflow'] == 'true':
            print('InfinStorArtifactRepository: usePresignedUrlForMLflow='
                    + str(rj['usePresignedUrlForMLflow']), flush=True)
            self.use_presigned_url_for_mlflow = True
        else:
            self.use_presigned_url_for_mlflow = False
        
        # default artifact location: infinstor-mlflow-artifacts/mlflow-artifacts/<user_name>/1/1-16705263394030000000004/sklearn-model/MLmodel
        # if create_experiment() specifies an artifact uri:  <experiment_artifiact_uri>/<run-id>/...
        #
        # Ugly, but we need to determine the run_id from the artifact URI.
        last_slash = artifact_uri.rfind('/')
        if last_slash == -1:
            raise ValueError('artifact_uri ' + str(artifact_uri) + ' does not include run_id')

        # Note that self.subpath_after_runid is relative to the run's artifact root URI.  
        success, self.this_run_id, self.path_upto_including_runid, self.subpath_after_runid = self.parse_run_id_from_uri(artifact_uri)
        if not success:
            raise ValueError('Unable to extract run_id from artifact_uri ' + str(artifact_uri))
        if self.use_presigned_url_for_mlflow:
            print('InfinStorArtifactRepository.initialized. artifact_uri=' + artifact_uri
                + ', run_id=' + self.this_run_id
                + ', path_upto_including_runid=' + str(self.path_upto_including_runid)
                + ', subpath_after_runid=' + str(self.subpath_after_runid))
        super().__init__(artifact_uri)

    def is_run_id_valid(self, run_id):
        ind = run_id.find('-')
        if ind == -1:
            return False
        try:
            exp_id = int(run_id[:ind])
            run_id_portion = int(run_id[ind+1:])
            return True
        except ValueError as verr:
            return False

    def parse_run_id_from_uri(self, artifact_uri:str) -> Tuple[bool, str, str]:
        """

        Args:
            artifact_uri (_type_): the expected format is similar to s3://<bucket>/path/to/run_id/sub_path/after/run_id
            
            Example URIs:        
                default URI: similar to s3://<bucket>/infinstor-mlflow-artifacts/mlflow-artifacts/<user_name>/1/1-16705263394030000000004/sklearn-model/MLmodel                
                if create_experiment() specifies an artifact uri:  <experiment_artifiact_uri>/<run-id>/...

        Returns:
            Tuple[bool, str, str, str]: returns the tuple success, run_id, path_upto_including_runid, subpath_after_run_id.  The subpath_after_run_id and path_upto_including_runid has no leading or trailing '/'
        """
        au_parts:list[str] = artifact_uri.lstrip('/').rstrip('/').split('/')
        # traverse each path element of the artifact_uri from right to left
        for ind in range(len(au_parts), 0, -1):
            run_id = au_parts[ind-1]
            
            # if element at 'ind-1' is a run_id
            if self.is_run_id_valid(run_id):
                subpath_after_runid = ''
                # get subpath_after_runid: traverse all elements of the artifact_uri after the run_id: from ind to len(au_parts). 'ind-1' is the run_id.
                for ind1 in range(ind, len(au_parts), 1):
                    subpath_after_runid = subpath_after_runid + '/' + au_parts[ind1]
                subpath_after_runid = subpath_after_runid.lstrip('/').rstrip('/')
                
                # get path_upto_runid.  'ind-1' is the index for run_id.  for an s3 url like s3://<bucket>/path/to/run_id/sub_path/after/run_id, the index[3:ind] returns [path, to, run_id]
                path_upto_including_runid:str = '/'.join(au_parts[3:ind])
                path_upto_including_runid.lstrip('/').rstrip('/')
                return True, run_id, path_upto_including_runid, subpath_after_runid
        return False, '', '', ''

    def _get_s3_client(self):
        if not self.use_presigned_url_for_mlflow:
            return super()._get_s3_client()
        return None
    
    @classmethod
    def pretty_print_prep_req(cls, req:requests.PreparedRequest):
        return '{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        )
    
    def _upload_file(self, s3_client, local_file:Union[str,pathlib.Path], bucket:str, key:str):
        """
        _summary_

        Args:
            s3_client (_type_): _description_
            local_file (Union[str,pathlib.Path]): local_file can be pathlib.Path: see tests/artifacts/test_artifacts.py::test_download_artifacts_with_dst_path()
            upload_bucket (str): _description_
            upload_key (str): this is derived from artifact_uri and is under artifact_uri.  See S3ArtifactRepository._upload_file() implementation

        Raises:
            MlflowException: _description_

        Returns:
            _type_: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super()._upload_file(s3_client, local_file, bucket, key)
        print('InfinStorArtifactRepository._upload_file: local_file=' + str(local_file)\
                + ', bucket=' + str(bucket) + ', key=' + key)
        (au_bucket, au_artifact_path) = data.parse_s3_uri(self.artifact_uri)
        self._verify_listed_object_contains_artifact_path_prefix(
            listed_object_path=key, artifact_path=au_artifact_path
        )
        if au_bucket != bucket:
            raise MlflowException(
                "InfinStorArtifactRepository:_upload_file bucket mismatch. artifact_bucket="\
                        + au_bucket + ", bucket in=" + bucket)
        
        # at this point we've verified that 
        # -- au_artifact_path has a run_id (stored in self.this_run_id and done by __init__() )
        # -- 'upload_key' is under 'au_artifact_path' 
        # -- and the au_bucket and upload_bucket are the same.
        # with this, we have verified that 'upload_bucket' and 'upload_key' represent a location under the run's artifact root URI.
        # 
        # Now get a new_key that is compliant with get_presigned_url() API
        success:bool; run_id:str; subpath_after_run_id:str
        success, run_id, _, subpath_after_run_id = self.parse_run_id_from_uri(f's3://{bucket}/{key}')
        ps_url = self.get_presigned_url(subpath_after_run_id, 'put_object')
        # open() accpets os.PathLike protocol: see https://docs.python.org/3/library/functions.html#open
        with open(local_file, 'rb') as fp:
            file_data = fp.read()
            hr:requests.Response = requests.put(ps_url, data=file_data)
            if (hr.status_code != 200):
                print(f'InfinStorArtifactRepository._upload_file: WARNING. upload resp != 200. response.status_code={hr.status_code};\n  response.content={hr.content};\n  response.headers={hr.headers};\n  response.request={InfinStorArtifactRepository.pretty_print_prep_req(hr.request)}')
    
    def _download_file(self, remote_file_path:str, local_path:Union[str,pathlib.Path]):
        """
        _summary_

        Args:
            remote_file_path (str): 'remote_file_path' is relative to 'artifact_uri'.  is is a path under under artifact_uri.  See S3ArtifactRepository._download_file() for details
            local_path (Union[str,pathlib.Path]): local_file can be pathlib.Path: see tests/artifacts/test_artifacts.py::test_download_artifacts_with_dst_path()

        Returns:
            _type_: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super()._download_file(remote_file_path, local_path)
        # Note: subpath_after_runid is relative to the run's artifact root URI (see __init__()).  so remote_file_path is also relative to the run's artifact root URI, is under the run's artifact root URI, which is what we want.
        remote_file_path = self.subpath_after_runid + '/' + remote_file_path if self.subpath_after_runid else remote_file_path
        print('InfinStorArtifactRepository._download_file: remote_file_path=' + str(remote_file_path) + ', local_path=' + str(local_path))
        ps_url = self.get_presigned_url(remote_file_path, 'get_object')
        urlretrieve(ps_url, local_path)

    def _is_directory(self, artifact_path:str) -> bool:
        """
        _summary_

        Args:
            artifact_path (str): relative to artifact_uri.  See ArtifactRepository._is_directory() for details.

        Returns:
            bool: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super()._is_directory(artifact_path)
        if not artifact_path:
            #print('InfinStorArtifactRepository._is_directory: True since no artifact_path')
            return True
        if artifact_path[-1] == '/':
            #print('InfinStorArtifactRepository._is_directory: True since artifact_path ends in /')
            return True
        # artifact_path is relative to artifact_uri and not the run's artifact root URI.  so convert it to a path relative to run's artifact root URI
        art_path_relative_to_run_root_uri = posixpath.join(self.subpath_after_runid, artifact_path) if self.subpath_after_runid else artifact_path
        ps_url = self.get_presigned_url(art_path_relative_to_run_root_uri, 'list_objects_v2')
        try:
            response = requests.get(ps_url)
            response.raise_for_status()
        except HTTPError as http_err:
            print('InfinStorArtifactRepository._is_directory: HTTP error occurred: '\
                    + str(http_err))
            raise
        except Exception as err:
            print('InfinStorArtifactRepository._is_directory: Other error occurred: ' + str(err))
            raise
        root:xml.etree.ElementTree.Element = ET.fromstring(response.content)
        for prefix_elem in root.findall('./aws:CommonPrefixes/aws:Prefix', namespaces={'aws':'http://s3.amazonaws.com/doc/2006-03-01/'}):
            # list_objects_v2(), for a given prefix, may result in a match that is not an exact match of 
            # path_upto_including_runid + '/' + art_path_relative_to_run_root_uri, since it is a prefix match.
            # 
            # for example, if the prefix is 'mlflow-artifacts/user/4/4-16xxxxxx004/estimator', it may match 
            #     'mlflow-artifacts/user/4/4-16xxxxxx004/estimator.html' (in Contents) and 
            #     'mlflow-artifacts/user/4/4-16xxxxxx004/estimator_1.html' (in Contents) and 
            #      mlflow-artifacts/user/4/4-16xxxxxx004/estimator/ (in CommonPrefixes).  
            #      mlflow-artifacts/user/4/4-16xxxxxx004/estimator_dup/ (in CommonPrefixes).  
            # 
            # So check for an exact match
            # 
            # 'CommonPrefixes': [{'Prefix': 'mlflow-artifacts/username/20/20-16781922633870000000007/train/estimator/'}, {'Prefix': 'mlflow-artifacts/username/20/20-16781922633870000000007/train/estimator_dup/'}]
            if prefix_elem.text and prefix_elem.text == self.path_upto_including_runid + '/' + art_path_relative_to_run_root_uri + '/': return True
            
        #print('InfinStorArtifactRepository._is_directory: False since at no common prefix is present')
        return False

    def list_artifacts(self, path:str) -> List[FileInfo]:
        """
        _summary_

        Args:
            path (str): this is relative to artifact_uri.  See S3ArtifactRepository.list_artifacts() for details

        Returns:
            List[FileInfo]: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super().list_artifacts(path=path)
        if not path:
            path = ''
        elif path[len(path) - 1] != '/':
            path = path + '/'
        # path is guaranteed to be a directory
        print('InfinStorArtifactRepository.list_artifacts: path=' + path + ', artifact_uri=' + str(self.artifact_uri))
        (au_bucket, au_artifact_path) = data.parse_s3_uri(self.artifact_uri)
        
        # get_presigned_url() expects a prefix relative to run's artifact root URI.  but 'path' is relative to 'artifact_uri'.  Translate it now
        path_rel_run_root_uri:str = self.subpath_after_runid + '/' + path if self.subpath_after_runid else path
        ps_url = self.get_presigned_url(path_rel_run_root_uri, 'list_objects_v2')
        try:
            response = requests.get(ps_url)
            response.raise_for_status()
        except HTTPError as http_err:
            print('list_artifacts: HTTP error occurred: ' + str(http_err))
            raise
        except Exception as err:
            print('list_artifacts: Other error occurred: ' + str(err))
            raise
        #print('InfinStorArtifactRepository.list_artifacts: resp=' + str(response.content))
        root = ET.fromstring(response.content)
        infos=[]
        for child in root:
            if (child.tag.endswith('CommonPrefixes')):
                for child1 in child:
                    fp = unquote(str(child1.text))
                    self._verify_listed_object_contains_artifact_path_prefix(
                        listed_object_path=fp, artifact_path=au_artifact_path
                    )
                    fp1 = fp[len(au_artifact_path)+1:]
                    fp2 = fp1.rstrip('/')
                    infos.append(FileInfo(fp2, True, None))
            elif (child.tag.endswith('Contents')):
                filesize = 0
                filename = None
                for child1 in child:
                    if child1.tag.endswith('Key'):
                        filename = child1.text
                    elif child1.tag.endswith('Size'):
                        filesize = int(child1.text)
                if filename:
                    fp = unquote(str(filename))
                    self._verify_listed_object_contains_artifact_path_prefix(
                        listed_object_path=fp, artifact_path=au_artifact_path
                    )
                    fp1 = fp[len(au_artifact_path)+1:]
                    fp2 = fp1.rstrip('/')
                    fp3 = fp2.lstrip('/')
                    infos.append(FileInfo(fp3, False, filesize))
        return infos

    def get_presigned_url(self, prefix:str, method:str):
        """
        _summary_

        Args:
            prefix (str): prefix is relative to the run's artifact root URI.
            method (str): s3 method such as 'put_object' or 'list_objects_v2' or others

        Returns:
            _type_: _description_
        """
        attempt = 0
        max_attempts = 3
        while attempt < max_attempts:
            if attempt == 0:
                force = False
            else:
                print('get_presigned_url: retrying')
                force = True
            attempt = attempt + 1
            token, service = get_token(builtins.region, force)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': token
                }
            url = 'https://' + builtins.mlflowserver\
                    + '/Prod/2.0/mlflow/artifacts/getpresignedurl'\
                    + '?run_id=' + self.this_run_id\
                    + '&path=' + quote(prefix)\
                    + '&method=' + method
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
            except HTTPError as http_err:
                print('get_presigned_url(): HTTP error occurred: ' + str(http_err))
                # if this is the last iteration of retrying, raise the exception; 'attempt' has already been incremented above, so comparision is >=, even though 'attempt' is zero based
                if attempt >= max_attempts: raise
            except Exception as err:
                print('get_presigned_url(): Other error occurred: ' + str(err))
                # if this is the last iteration of retrying, raise the exception; 'attempt' has already been incremented above, so comparision is >=, even though 'attempt' is zero based
                if attempt >= max_attempts: raise
            if 'Login expired. Please login again' in response.text:
                continue
            js = response.json()
            return js['presigned_url']
        print('get_presigned_url: Tried twice. Giving up')
        return None

