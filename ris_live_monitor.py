#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import websocket
import sys
import time
import boto3


def parse_args():
	parser = argparse.ArgumentParser()
	# This is a CAIDA AS topology.
	parser.add_argument("-a", "--asns",
						default=[1234], nargs='*', type=int)
	parser.add_argument("-p", "--single_peer",
						default="2914", nargs='*')
	return parser.parse_args()


def main(args):
	ws = websocket.WebSocket()
	ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-example-1")
	params = {
		#"prefix": prefix,
		"prefix": None,
		"moreSpecific": True,
		#"host": None,
		"host": "rrc12.ripe.net", # None means all collectors.
		"socketOptions": {
			"includeRaw": True,
			"acknowledge": True
		}
	}
	ws.send(json.dumps({
		"type": "ris_subscribe",
		"data": params
	}))
	
	recordCounter = 0

	client = boto3.client('sns')

	
	#sns.publish_message("bgp-alert", "test", {})a
	for data in ws:

		parsed = json.loads(data)
		#print(parsed["type"], parsed["data"])
		if parsed["type"] == "ris_subscribe_ok":
			print(parsed["type"], parsed["data"])
		elif parsed["type"] == "ris_message":# and 'withdrawals' not in parsed["data"]:
			if args.single_peer != "":
				if parsed["data"]["peer_asn"] != args.single_peer:
					continue
			if "announcements" in parsed["data"]:
				for announcement in parsed["data"]["announcements"]:
					recordCounter += 1
					if recordCounter % 100 == 0:
						print(f"[info {time.time()}] Processed {recordCounter} records", file=sys.stderr)
					#print(parsed["type"], parsed["data"])
					for asn in args.asns:
						if asn in parsed["data"]["path"]:
							print(parsed["type"], parsed["data"])
							response = client.publish(
    							TopicArn='your-topic-arn-here',
    							Message=str(parsed["data"]),
    							Subject='BGP Monitoring Alert')

			#if "withdrawals" in parsed["data"]:
			#	if prefix in parsed["data"]["withdrawals"] or subprefix in parsed["data"]["withdrawals"]:
			#		print(parsed["type"], parsed["data"])
			
			#print(parsed["type"], parsed["data"])
			#try:
			#	asLength = len(parsed["data"]["path"])
			#	if asLength > maxASLength:
			#		maxASLength = asLength
			#	print(maxASLength)
			#except:
			#	print(parsed["type"], parsed["data"])



if __name__ == '__main__':
	main(parse_args())
