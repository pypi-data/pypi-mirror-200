import consul
import json
import uuid
import logging
import sys

sys.path.append('../../')
from inhand.service.SettingService import SpringCloudSettings, Consul

class ConsulService(object):
    def __init__(self, host, port):
        '''初始化，连接consul服务器'''
        self._consul = consul.Consul(host, port)

    def __buildApiConfiguation(self, local_ip, port, app_name, app_id, prefix, app_group, instance_info, apis, protocol='http',health_entry='/health'):
        tags = []

        tags.append("group={}".format(app_group))
        tags.append("secure=false")
        tags.append("{}.enable=true".format(prefix))
        tags.append("{}.http.services.{}.loadbalancer.server.weight=1".format(prefix, app_name))
        tags.append("{}.http.services.{}.loadbalancer.passHostHeader=true".format(prefix, app_name))
        tags.append("{}.http.services.{}.loadbalancer.server.scheme={}".format(prefix, app_name,protocol))
        tags.append("{}.instance={}".format(app_id, json.dumps(instance_info)))

        for api in apis:
            uid = str(uuid.uuid4())
            suid = ''.join(uid.split("-"))
            route_prefix = "{}.http.routers.{}".format(prefix, suid)
            tags.append("{}.rule=Path(`{}`) && Method(`{}`)".format(route_prefix, api['path'], api['method']))
            key = None
            if 'scope' in api.keys():
                key = 'scope'
            elif 'scopes' in api.keys():
                key = 'scopes'
            if key is not None:
                tags.append("{}.middlewares=nezha@internal".format(route_prefix))
                tags.extend(
                    ["{}.metadata.nezha.scopes={}".format(route_prefix, scope) for scope in api[key].split(',')])

        logging.info("Tags:" + str(tags))
        api_info={"tags": tags,"local_ip":local_ip,"port":port,"app_id":app_id,"app_name":app_name,"app_group":app_group,"instance_info":instance_info,"protocol":protocol,"health_entry":health_entry}
        return api_info

    """
    def registerAPI(self, data):
        #data=self.buildApiConfiguation(local_ip,port,app_name,app_id,perfix,app_group,instance_info,apis,protocol,health_entry)

        self.registerService(data['app_name'], data['app_id'], data['local_ip'], data['port'], tags=data['tags'], protocol=data['protocol'],
                             health_entry=data['health_entry'])

        svc,res = self.getService(data['app_id'])
        logging.info(str(svc))
    """

    def registerService(self, name, service_id, host, port, tags=None, protocol='http', health_entry='/health'):
        tags = tags or []
        url = "{}://{}:{}{}".format(protocol, host, port, health_entry)
        logging.info("Health Url: {}".format(url))
        # 注册服务
        self._consul.agent.service.register(
            name=name,
            service_id=service_id,
            address=host,
            port=port,
            tags=tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
            check=consul.Check().http(url, "5s", "30s", "30s", None))

    def check(self, host, port, interval, timeout=None, deregister=None, header=None, health_entry='/health',
              protocol='http'):
        return consul.Check.http("{}}://{}:{}{}".format(protocol, host, port, health_entry), interval, timeout,
                                 deregister, header)

    def getService(self, servie_id):
        services = self._consul.agent.services()
        service = services.get(servie_id)
        if not service:
            return None, None
        addr = "{0}:{1}".format(service['Address'], service['Port'])
        return service, addr

    def registerNezhaApi(self,consul,settings):
        local_ip = Utility.getLocalIP(host=consul.host,port=consul.port)
        port = settings.port
        app_name = settings.name
        app_id = '{}-{}'.format(app_name, local_ip.replace(".", "-"))
        prefix = settings.prefix
        tags = []

        tags.append("group={}".format(consul.instance_group))
        tags.append("secure=false")
        tags.append("{}.enable=true".format(prefix))
        tags.append("{}.http.services.{}.loadbalancer.server.weight=1".format(prefix, app_name))
        tags.append("{}.http.services.{}.loadbalancer.passHostHeader=true".format(prefix, app_name))
        tags.append("{}.instance={}".format(app_id, json.dumps(settings['instance_info'].toMap())))

        for api in settings['api_info'].apis:
            uid = str(uuid.uuid4())
            suid = ''.join(uid.split("-"))
            api_prefix = '{}.http.routers.{}'.format(prefix, suid)
            tags.append("{}.rule=Path(`{}`) && Method(`{}`)".format(api_prefix, api['path'], api['method']))
            if ('scope' in api.keys()):
                tags.append("{}.metadata.nezha.scopes={}".format(api_prefix, api['scope']))
                tags.append("{}.middlewares=nezha@internal`)".format(api_prefix))

        consul_service = ConsulService(consul.host,consul.port)
        res = consul_service.registerService(app_name, app_id, local_ip, port, tags)

        # check=consul_service.check()
        # print(check)
        res = consul_service.getService(app_id)
        print(res)

if __name__ == '__main__':

    from inhand.utilities.Utility import Utility
    settings=SpringCloudSettings()
    settings.readBootstrapYaml("d:\\bootstrap.yml")

    api_entries = [
        {
            "desc": "获取老化车信息",
            "path": "/api/v1.0/aging_car/info",
            "method": "GET",
            "scope": "mes:aging:get"
        },
        {
            "desc": "获取老化信息",
            "path": "/api/v1.0/aging/query",
            "method": "GET",
            "scope": "mes:aging:get"
        },
        {
            "desc": "序列号绑定老化车",
            "path": "/api/v1.0/aging/sn_bind",
            "method": "POST",
            "scope": "mes:aging:post"
        },
        {
            "desc": "工单绑定老化车",
            "path": "/api/v1.0/aging/order_bind",
            "method": "POST",
            "scope": "mes:aging:post"
        }
    ]
    consulService = ConsulService(settings.consul.host, settings.consul.port)
    data=consulService.__buildApiConfiguation("10.5.84.37", 8069,'odoo-api','odoo-api-10-5-84-37', 'traefik', 'inhand-poweris',
                              {'verison':'v1.0.0'}, api_entries, protocol='http',
                    health_entry='/health')
    with open('./api-info.json','w') as f:
        json.dump(data,f)

    with open('./api-info.json','r') as f:
        data1=json.load(f)
    consulService.registerAPI(data1)



    """
    tags=[]
    tags.append("group=inhand-poweris")
    tags.append("secure=flaes")
    tags.append("traefik.enable=true")

    tags.append("traefik.http.services.jx-attendance-api.loadbalancer.server.weight=1")
    consulService=ConsulService("consul",8500)
    name="jx-attandance-api-10-0-0-1"
    service_id="jx-attendance-api"
    consulService.registerService(name,service_id,"10.5.0.247",5000,tags)

    check=consulService.check("10.5.0.247",5000,"30s")
    print(check)
    res=consulService.getService(service_id)
    print(res)
    """


