

### bloco - apaga fluxo  ###


curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0'
sleep 1
curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/table/0'
sleep 1
curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:3/table/0'
sleep 1
curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:4/table/0'
sleep 1
curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:5/table/0'
sleep 1
curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:6/table/0'
sleep 1
curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:7/table/0'
sleep 1
curl -v --user "admin":"admin" -X DELETE 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:8/table/0'
sleep 1
