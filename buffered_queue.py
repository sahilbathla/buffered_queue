#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from utils.redis_queue import RedisQueue
from kafka import KafkaProducer
import SocketServer
import random
import simplejson
import yaml

with open('config/conf.yaml', 'r') as stream:
    try:
        config = (yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)

class Server(BaseHTTPRequestHandler):

    def validate_data(self, data):
        if not data.get('group_id'):
            print "Group Id is missing"
            return False
        else:
            return True

    def push_data(self, q):
        topic = q.get_topic()
        payload = q.get_all()
        if (topic):
            try:
                producer = KafkaProducer(bootstrap_servers=config.get('bootstrap_servers').split(','))
                producer.send(bytes(topic), bytes(payload))
                return True
            except Exception as e:
                print "Kafka Error: %s" %(format(e))
        else:
            print "Topic is not defined for this group %s" %q.get_key()
            return False

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        try:
            data = simplejson.loads(self.data_string)
            if (self.validate_data(data)):
                group_id = data.get(config.get('group_segregator'))
                q = RedisQueue(group_id, host=config.get('redis_host'), port=config.get('redis_port'))
                q.put(data)
                print "Queue Size: %s for Group %s" %(q.qsize(), group_id)
                if int(q.qsize()) >= q.get_limit():
                    if self.push_data(q):
                        print "Buffer cleared and pushed to kafka topic %s for group %s" %(q.get_topic(), group_id)
                        q.empty()
                    else:
                        print "Could not push data to kafka topic %s for group %s" %(q.get_topic(), group_id)
        except Exception as e:
            print "Malformed input %s" %(format(e))
        return


def run(server_class=HTTPServer, handler_class=Server, port=8082):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

run()
