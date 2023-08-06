import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Union, List
from urllib.parse import urljoin

import requests
import urllib3
from com.vmware.vcenter.vm.hardware_client import Ethernet
from com.vmware.vcenter.vm_client import Power as HardPower
from com.vmware.vcenter_client import Folder, VM, Network
from vmware.vapi.vsphere.client import create_vsphere_client

from config import Config
from tools.consts import STATE_TIMEOUT, autotests_folders
from tools.helpers import get_network_backing

_ROOT_DIR = Path(__file__).parent
DEFAULT_CREDENTIALS = Path(_ROOT_DIR / 'tools/vmrest.cfg')

class VMwareNodeVsphere:
    def __init__(self, node_ip: str = ''):
        session = requests.session()
        session.verify = False
        self.hostname = Config.hostname
        self.datacenter = Config.datacenter
        self.cluster = Config.cluster
        self.resource_pool = Config.resource_pool
        self.username = Config.username
        self.password = Config.password
        self.datastore = Config.datastore

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.client = create_vsphere_client(server=self.hostname, username=self.username,
                                            password=self.password, session=session)
        self.node_ip = node_ip
        self.vlan200_network_id = get_network_backing(self.client, 'VLAN200', self.datacenter,
                                                      Network.Type.DISTRIBUTED_PORTGROUP)

        try:
            self.vm = [vm for vm in self.vms_in_folders(folder_names=autotests_folders) if
                       '.'.join(node_ip.split('.')[2:]) in vm.name][-1]
        except IndexError:
            raise AssertionError(f"There's no vm with ip {self.node_ip} in folders {', '.join(autotests_folders)} at vSphere")
        self.nic_summaries = self.client.vcenter.vm_settings.hardware.Ethernet.list(vm=self.vm.vm_settings)

    def manage_nic(self, connect: bool):
        if connect:
            self.client.vcenter.vm_settings.hardware.Ethernet.connect(self.vm.vm_settings, self.nic_summaries[-1].nic)
        else:
            self.client.vcenter.vm_settings.hardware.Ethernet.disconnect(self.vm.vm_settings,
                                                                         self.nic_summaries[-1].nic)

    def change_nic_to_vlan200(self, nic):
        nic_settings = Ethernet.UpdateSpec(
            allow_guest_control=True,
            start_connected=True,
            upt_compatibility_enabled=False,
            wake_on_lan_enabled=True,
            backing=Ethernet.BackingSpec(type=Ethernet.BackingType.DISTRIBUTED_PORTGROUP,
                                         network=self.vlan200_network_id))
        self.client.vcenter.vm_settings.hardware.Ethernet.update(self.vm.vm_settings, nic, nic_settings)

    def is_working(self):
        status = self.client.vcenter.vm_settings.Power.get(self.vm.vm_settings)
        if status == HardPower.Info(state=HardPower.State.POWERED_ON):
            return True
        elif status == HardPower.Info(state=HardPower.State.POWERED_OFF):
            return False

    def power_off(self):
        if self.is_working():
            self.client.vcenter.vm_settings.Power.stop(self.vm.vm_settings)
        else:
            AssertionError(f'Virtual machine {self.node_ip} is off! '
                           f'State: {self.client.vcenter.vm_settings.Power.get(self.vm.vm_settings)}')

    def power_on(self):
        if not self.is_working():
            self.client.vcenter.vm_settings.Power.start(self.vm.vm_settings)
        else:
            AssertionError(f'Virtual machine {self.node_ip} is on! '
                           f'State: {self.client.vcenter.vm_settings.Power.get(self.vm.vm_settings)}')
        # wait_for_guest_power_state(self.client, self.vm, Power.State.RUNNING, STATE_TIMEOUT)

    def reboot(self):
        self.client.vcenter.vm_settings.guest.Power.manual_reboot(self.vm.vm_settings)

    def wait_for_power_operations_state(self, desiredState: bool, timeout: int = STATE_TIMEOUT):
        """
        Waits for the guest to reach the desired power state, or times out.
        """
        print("Waiting for guest power state {}".format(desiredState))
        start = time.time()
        timeout = start + timeout
        while timeout > time.time():
            time.sleep(1)
            curState = self.client.vcenter.vm_settings.guest.Power.get(self.vm.vm_settings).state
            if desiredState == curState:
                break
        if desiredState != curState:
            raise AssertionError('Timed out waiting for guest to reach desired power state')
        else:
            AssertionError(f'Took {time.time() - start} seconds for guest power state to change to {desiredState}')

    def vms_in_folders(self, folder_names=autotests_folders):
        folder_filter = Folder.FilterSpec(names=set(folder_names))
        folder_id_list = [elem.folder for elem in self.client.vcenter.Folder.list(folder_filter)]
        vm_filter = VM.FilterSpec(folders=set(folder_id_list))
        return self.client.vcenter.VM.list(vm_filter)

class VMwareLocalApi:
    PLATFORM = sys.platform
    if PLATFORM == 'linux':
        CONFIG_PATH = subprocess.Popen(
            r'echo 111111 | sudo find /home -name .vmrestCfg 2>/dev/null', shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.read().decode('utf-8').strip()
        BINARY_PATH = subprocess.Popen(
            r'echo 111111 | sudo find /usr/bin/ -name vmrest 2>/dev/null', shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.read().decode('utf-8').strip()
        OVF_TOOL = subprocess.Popen(
            r'echo 111111 | sudo find /usr/bin/ -name ovftool 2>/dev/null', shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    elif PLATFORM == 'win32':
        CONFIG_PATH = subprocess.Popen(r'dir /s /b "C:\Users\vmrest.cfg"', shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).stdout.read().decode('cp1251').strip()
        BINARY_PATH = subprocess.Popen(
            r'dir /s /b "C:\Program Files (x86)\vmrest.exe"', shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.read().decode('cp1251').strip()
        OVF_TOOL = subprocess.Popen(
            r'dir /s /b "C:\Program Files (x86)\ovftool.exe"', shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.read().decode('cp1251').strip()
    else:
        raise AssertionError('Unknown OS')
    assert all([CONFIG_PATH, BINARY_PATH,
                OVF_TOOL]), f"Can't find one of these files: {[CONFIG_PATH, BINARY_PATH, OVF_TOOL]}"

    def __init__(self, new_cred_config_path=DEFAULT_CREDENTIALS, binary=None, config=None, ovf_tool=None, debug=False, port=None):
        self.session = requests.Session()
        self.session.auth = ('root', 'Root_12345')
        self.session.headers['Content-Type'] = 'application/vnd.vmware.vmw.rest-v1+json'
        self.proc = None
        self.args = list()
        self.is_linux = sys.platform == 'linux'
        self.encoding = 'utf-8' if self.is_linux else 'cp1251'
        self.host_user = self.get_host_username()
        self.binary = binary or VMwareLocalApi.BINARY_PATH
        self.config = config or VMwareLocalApi.CONFIG_PATH
        self.ovf_tool = ovf_tool or VMwareLocalApi.OVF_TOOL
        self.replace_auth_cfg(new_cred_config_path)
        self.ip_address = f'http://127.0.0.1:{port or "8697"}/api/'
        if debug:
            self.args.append('--debug')
        if port:
            self.args.append(f'--port {port}')
        self.start_process()

    @staticmethod
    def check_status_code(func):

        def wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            if not response.ok:
                raise AssertionError(f'status_code: {response.status_code}, msg: {response.text}')
            try:
                res = json.loads(response.text)
                return res
            except json.JSONDecodeError:
                return response.text

        return wrapper

    def get_host_username(self):
        output = subprocess.Popen(['whoami'], shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.read().decode(self.encoding).strip()
        return output if self.is_linux else output.split('\\')[-1]

    def replace_auth_cfg(self, new_config_path: Union[str, Path]):
        util = 'cat' if self.is_linux else 'type'
        subprocess.Popen([util, str(new_config_path), '>', self.config], shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    def start_process(self):
        self.proc = subprocess.Popen([self.binary] + self.args, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

    def kill_process(self):
        stdout, stderr = self.proc.communicate()
        self.proc.terminate()
        if self.proc.returncode != 5:
            print(stderr)

    def api_path(self, endpoint, path_params):
        try:
            path_params.pop('self')
            path_params.pop('data')
        finally:
            return urljoin(self.ip_address, endpoint.format(**path_params if path_params else {}))

    @check_status_code
    def _request(self, method: str, endpoint: str, path_params: dict = None, json: Union[dict, List[dict]] = None,
                 data: str = None):
        if json:
            json = {k: v for k, v in json.items() if v not in ['self', 'vm_id', None]}
        return self.session.request(method, self.api_path(endpoint, path_params), json=json, data=data)


class VmManage(VMwareLocalApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_base = 'vms'

    @property
    def vm_list(self):
        return self._request('get', self.api_base)

    def vm_info(self, vm_id: str):
        return self._request('GET', self.api_base + '/{vm_id}/restrictions', path_params=locals())

    def vm_settings(self, vm_id: str):
        return self._request('GET', self.api_base + '/{vm_id}', path_params=locals())

    def update_vm_settings(self, vm_id: str, processors: int = None, ram_memory: int = None):
        return self._request('PUT', self.api_base + '/{vm_id}', path_params={'vm_id': vm_id},
                             json={'processors': processors,
                                   'memory': ram_memory})

    # ============ Not sure how it's working ===========
    def congif_param(self, vm_id: str, name: str):
        return self._request('GET', self.api_base + '/{vm_id}/params/{name}', path_params=locals())

    def update_vm_config(self, vm_id: str, params: List[dict]):
        """Example: [{"name": "string", "value": "string"}, {"name": "string", "value": "string"}]"""
        return self._request('PUT', self.api_base + '/{vm_id}', path_params={'vm_id': vm_id}, json=params)

    # ===============================================

    def copy_vm(self, name: str, parent_vm_id: str):
        r"""Copying to default folders. Windows: \Users\{user}\Documents\Virtual Machines
                                          Linux: /var/lib/vmware/Virtual Machines"""
        return self._request('POST', self.api_base, json={'name': name, 'parentId': parent_vm_id})

    def register_vm(self, name: str, path: Union[str, Path]):
        """Needed path with escapes. Example: C:\\Users\\user\\Downloads\\test\\my.vmx
        :param name: VM name
        :param path: Path to vmx file"""
        return self._request('POST', self.api_base + '/registration', json={'name': name, 'path': str(path)})

    def delete_vm(self, vm_id: str):
        return self._request('DELETE', self.api_base + '/{vm_id}', path_params=locals())


class VmNetwork(VMwareLocalApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_base = 'vms/{vm_id}/nic'

    def vm_ip(self, vm_id: str):
        return self._request('GET', self.api_base[:-3] + 'ip', path_params=locals())

    def nics(self, vm_id: str):
        return self._request('GET', self.api_base, path_params=locals())['nics']

    def create_nic(self, vm_id: str, nic_type: str, vmnet: str):
        return self._request('POST', self.api_base, path_params=locals(), json={'type': nic_type, 'vmnet': vmnet})

    def update_nic(self, vm_id: str, nic_index: int, nic_type: str, vmnet: str = None):
        return self._request('PUT', self.api_base + '/{nic_index}', path_params=locals(),
                             json={'type': nic_type, 'vmnet': vmnet})

    def delete_nic(self, vm_id: str, nic_index: int):
        return self._request('DELETE', self.api_base + '/{nic_index}', path_params=locals())


class VmPowerState(VMwareLocalApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_base = 'vms/{vm_id}/power'

    def state(self, vm_id: str):
        return self._request('GET', self.api_base, path_params=locals())

    def power_on(self, vm_id: str, power_on: bool):
        return self._request('PUT', self.api_base, path_params=locals(), data='on' if power_on else 'off')

    @staticmethod
    def wait_state_change(vm_id, power_on: bool, time_out=60):
        param = '-c' if sys.platform == 'linux' else '-n'
        while time_out:
            time_out -= 2
            command = os.system(f'ping {param} 1 {vm_id}')
            if power_on and not command:
                return
            elif not power_on and command:
                return
            time.sleep(2)
        raise AssertionError(f'Virtual machine {vm_id} is unreachable for {time_out} seconds!')


class VmSharedFolders(VMwareLocalApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_base = 'vms/{vm_id}/sharedfolders'

    def list(self, vm_id: str):
        return self._request('GET', self.api_base, path_params=locals())

    def mount_folder(self, vm_id: str, folder_id: str, folder_path: str, read_only: bool):
        return self._request('POST', self.api_base, path_params=locals(),
                             json={'folder_id': folder_id, 'host_path': folder_path,
                                   'flags': 0 if read_only else 4})

    def update_folder(self, vm_id: str, folder_id: str, folder_path: str, read_only: bool):
        return self._request('PUT', self.api_base + '/{folder_id}', path_params=locals(),
                             json={'host_path': folder_path, 'flags': 0 if read_only else 4})

    def delete_folder(self, vm_id: str, folder_id: str):
        return self._request('DELETE', self.api_base + '/{folder_id}', path_params=locals())


class VirtualNetworks(VMwareLocalApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_base = 'vmnet'

    @property
    def list(self):
        return self._request('GET', self.api_base, path_params=locals())

    def create_virtual_network(self, name: str, type: str):
        """
        :param name: Virtual network name
        :param type: One of: bridged, nat, hostonly
        """
        if type not in ['bridged', 'nat', 'hostonly']:
            raise AssertionError(f"Network type {type} isn't correct")
        return self._request('POST', self.api_base + 's', path_params=locals())

    def mac_to_ip(self, vm_network: str):
        """:param vm_network: Virtual network that has DHCP enabled"""
        return self._request('GET', self.api_base + '/{vm_network}/mactoip', path_params=locals())

    def update_mac_to_ip(self, vm_network: str, mac: str, ip: str):
        """
        :param vm_network: Virtual network that has DHCP enabled
        :param mac: Mac address that want to be mapped with a given IP
        :param ip: IP that will be assigned to given Mac address.
        If empty IP, the original Mac to IP binding will be deleted
        """
        return self._request('PUT', self.api_base + '/{vm_network}/mactoip/{mac}', path_params=locals(),
                             json={'IP': ip})

    def port_forward(self, vm_network: str):
        """:param vm_network: NAT type of virtual network"""
        return self._request('GET', self.api_base + '/{vm_network}/portforward', path_params=locals())

    def update_port_forward(self, vm_network: str, protocol: str, port: int, guest_ip: str, guest_port: int, desc: str):
        """
        :param vm_network: NAT type of virtual network
        :param protocol: Protocol type: tcp, udp
        :param port: Host port number
        :param guest_port: Guest port to forward to
        :param guest_ip: Guest ip to forward to
        :param desc: Description
        """
        return self._request('PUT', self.api_base + '/{vm_network}/portforward/{protocol}/{port}', path_params=locals(),
                             json={"guestIp": guest_ip, "guestPort": guest_port, "desc": desc})

    def delete_port_forward(self, vm_network: str, protocol: str, port: int):
        """
        :param vm_network: NAT type of virtual network
        :param protocol: Protocol type: tcp, udp
        :param port: Host port number
        """
        return self._request('DELETE', self.api_base + '/{vm_network}/portforward/{protocol}/{port}',
                             path_params=locals())


class VMwareNodeLocal:

    def __init__(self, binary=None, config=None, ovf_tool=None, debug=False, port=None):
        self.vms_manage = VmManage(binary, config, ovf_tool, debug, port)
        self.vms_network = VmNetwork(binary, config, ovf_tool, debug, port)
        self.vms_power = VmPowerState(binary, config, ovf_tool, debug, port)
        self.vms_shared_folders = VmSharedFolders(binary, config, ovf_tool, debug, port)
        if VMwareLocalApi.PLATFORM != 'linux':
            self.host_network = VirtualNetworks(binary, config, ovf_tool, debug, port)

    def deploy_ova(self, ova_path: Path, vm_folder: str, vm_name: str) -> dict:
        vmware = self.vms_manage
        result = subprocess.Popen([vmware.ovf_tool, ova_path, vm_folder], shell=True,
                                  stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = result.communicate()
        result.wait()
        if result.returncode != 0:
            raise AssertionError(stderr.decode(vmware.encoding), stdout.decode(vmware.encoding))
        return vmware.register_vm(vm_name, Path(vm_folder, ova_path.name[:-4], ova_path.name[:-4] + '.vmx'))