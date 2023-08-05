#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import copy
import inspect
import json
import math
import os
import random
import string
import sys
import threading
import time
from hashlib import sha256

import requests

from naruno.api.main import start
from naruno.blockchain.block.block_main import Block
from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger
from naruno.lib.perpetualtimer import perpetualTimer
from naruno.lib.settings_system import baklava_settings
from naruno.lib.settings_system import the_settings
from naruno.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from naruno.transactions.my_transactions.sended_transaction import \
    SendedTransaction
from naruno.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from naruno.transactions.transaction import Transaction
from naruno.wallet.wallet_import import Address
from naruno.wallet.wallet_import import wallet_import

logger = get_logger("REMOTE_APP")


class splitted_data:

    def __init__(self, split):
        self.split = split
        self.main_data = None
        self.validated = False
        self.data = []
        self.data_original = []


class Integration:

    def __init__(
        self,
        app_name,
        host="localhost",
        port=8000,
        password="123",
        sended=False,
        sended_not_validated=False,
        cache_true=True,
        wait_amount=None,
        checking=True,
    ):
        """
        :param host: The host of the node
        :param port: The port of the node
        :param password: The password of the wallet
        """
        self.app_name = app_name
        self.cache_name = sha256(
            self.app_name.encode()).hexdigest() + wallet_import(-1, 3)
        self.host = host
        self.port = port

        self.api = None

        if not self.check_api():
            self.start_api()

        self.password = password

        self.sended = sended

        self.sended_not_validated = sended_not_validated

        self.cache_true = cache_true

        self.last_sended = 0

        if wait_amount is None:
            self.wait_amount = Block("Onur").block_time * 2.5
        else:
            self.wait_amount = wait_amount

        self.get_cache()

        backup_host = copy.copy(self.host)
        backup_port = copy.copy(self.port)
        if the_settings()["baklava"]:
            self.host = "test_net.1.naruno.org"
            self.port = 8000

        self.max_tx_number = int(
            self.prepare_request(
                "/blockmaxtxnumber/get/",
                type="get",
            ).text)
        self.max_data_size = int(
            self.prepare_request(
                "/blockmaxdatasize/get/",
                type="get",
            ).text)

        self.host = backup_host
        self.port = backup_port

        self.sended_txs = []

        self.checking = checking

        logger.info(f"Integration of {self.app_name} is started")

    def check_api(self):
        try:
            self.prepare_request("/", "get")
            return True
        except Exception as e:
            return False

    def start_api(self):
        backup = sys.argv
        sys.argv = [sys.argv[0]]

        self.api = start(host=self.host, port=self.port, test=True)

        self.api_thread = threading.Thread(target=self.api.run)
        self.api_thread.start()
        sys.argv = backup

    def close(self):
        if self.api is not None:
            self.api.close()

    def disable_cache(self):
        self.cache_true = False
        self.cache = []

    def get_cache(self):
        if self.cache_true == False:
            self.cache = []
            return

        os.chdir(get_config()["main_folder"])

        if not os.path.exists(f"db/remote_app_cache/{self.cache_name}.cache"):
            self.cache = []
            self.save_cache()
        with open(f"db/remote_app_cache/{self.cache_name}.cache",
                  "r") as cache:
            self.cache = json.load(cache)

        self.backward_support_cache()
        self.save_cache()

    def backward_support_cache(self):
        for each_cache in self.cache:
            if len(self.cache[self.cache.index(each_cache)]) != 96:
                # remoe the cache
                self.cache.remove(each_cache)

    def save_cache(self):
        if self.cache_true == False:
            self.get_cache()
            return
        self.backward_support_cache()
        os.chdir(get_config()["main_folder"])
        with open(f"db/remote_app_cache/{self.cache_name}.cache",
                  "w") as cache:
            json.dump(self.cache, cache)

    def delete_cache(self):
        os.chdir(get_config()["main_folder"])
        os.remove(f"db/remote_app_cache/{self.cache_name}.cache")

    def prepare_request(self, end_point, type, data=None) -> requests.Response:
        """
        :param end_point: The end point of the request
        :param type: The type of the request (get, post)
        :param data: The data of the request
        :return: The response of the request
        """
        api = f"http://{self.host}:{self.port}"
        response = None
        if type == "post":
            response = requests.post(api + end_point, data=data)
        elif type == "get":
            response = requests.get(api + end_point)

        return response

    def send_forcer(self, action, app_data, to_user, retrysecond):
        stop = False
        while stop == False:
            stop = self.send(action, app_data, to_user, force=False)
            time.sleep(retrysecond)

    def send(self,
             action,
             app_data,
             to_user,
             amount=None,
             force=True,
             retrysecond=10) -> bool:
        """
        :param action: The action of the app
        :param app_data: The data of the app
        :param to_user: The user to send the data to
        """
        if time.time() - self.last_sended < self.wait_amount:
            time.sleep(self.wait_amount - (time.time() - self.last_sended))

        backup_host = copy.copy(self.host)
        backup_port = copy.copy(self.port)
        if the_settings()["baklava"]:
            self.host = "test_net.1.naruno.org"
            self.port = 8000

        self.host = backup_host
        self.port = backup_port

        data = {"action": self.app_name + action, "app_data": app_data}

        system_length = len(
            json.dumps({
                "action": self.app_name + action,
                "app_data": ""
            }))

        true_length = (self.max_data_size / self.max_tx_number -
                       system_length) - 10

        if len(app_data) > true_length:
            backup_checking = copy.copy(self.checking)
            self.checking = False
            # generate random charactere
            rando = ""
            for i in range(5):
                rando += random.choice(string.ascii_letters)

            split_random = rando + "-"

            self.send(
                action=action,
                app_data=f"split-0-{split_random}",
                to_user=to_user,
                force=force,
                retrysecond=retrysecond,
            )
            len_split_char = len(f"split--{split_random}-")

            total_size_of_an_data = len(
                app_data) + len_split_char + system_length

            how_many_parts = (
                int(math.ceil(
                    (len(app_data) + len_split_char) / true_length)) + 1)

            how_many_parts = int(
                math.ceil(
                    (len(app_data) + len_split_char + len(str(how_many_parts)))
                    / true_length))

            splitted_data = []
            split_length = true_length - len_split_char

            for i in range(how_many_parts):
                # split to part of app_data and app_data is an string
                part = app_data[i * int(split_length):i * int(split_length) +
                                int(split_length)]

                splitted_data.append(part)

            for each_data in splitted_data:
                self.send(
                    action=action,
                    app_data=
                    f"split-{2+splitted_data.index(each_data)}-{split_random}{each_data}",
                    to_user=to_user,
                    force=force,
                    retrysecond=retrysecond,
                )

            self.checking = backup_checking
            self.checker()

            self.send(
                action=action,
                app_data=f"split-1-{split_random}",
                to_user=to_user,
                force=force,
                retrysecond=retrysecond,
            )
            return True

        data = json.dumps(data)

        request_body = {
            "password": self.password,
            "to_user": to_user,
            "data": data,
        }

        self.sended_txs.append(
            [action, app_data, to_user, amount, force, retrysecond, data])

        if amount is not None:
            request_body["amount"] = amount

        response = self.prepare_request("/send/",
                                        type="post",
                                        data=request_body)

        if "false" in response.text:
            logger.error("Error sending message")
            if force:
                logger.info("Trying to send again")
                return self.send_forcer(action, app_data, to_user, retrysecond)
            return False
        else:
            logger.info(
                f"Message sent: app_name:{self.app_name} action:{action} data: {data} to: {to_user}"
            )
            self.last_sended = time.time()
            if self.checking:
                self.checker()
            return True

    def checker(self):
        time.sleep(self.wait_amount)
        backup_caches = copy.copy(self.cache)
        backup_sended_not_validated = copy.copy(self.sended_not_validated)
        backup_sended = copy.copy(self.sended)
        self.sended_not_validated = False
        self.sended = True
        self.cache = []
        self.save_cache()
        new_txs = self.get(get_all=True)

        for sended_tx in self.sended_txs[:]:
            in_get = False
            self.sended_txs.remove(sended_tx)
            for vaidated_tx in new_txs:
                if (vaidated_tx["toUser"] == sended_tx[2]
                        and vaidated_tx["data"]["action"] == json.loads(
                            sended_tx[6])["action"]
                        and vaidated_tx["data"]["app_data"] == json.loads(
                            sended_tx[6])["app_data"]):
                    in_get = True

            if not in_get:
                self.send(
                    sended_tx[0],
                    sended_tx[1],
                    sended_tx[2],
                    sended_tx[3],
                    sended_tx[4],
                    sended_tx[5],
                )

        self.cache = backup_caches
        self.save_cache()
        self.sended_not_validated = backup_sended_not_validated
        self.sended = backup_sended

    def get_(self, get_all):
        self.get_cache()
        response = self.prepare_request("/transactions/received", type="get")
        transactions = response.json()

        transactions_sended = {}
        transactions_sended_not_validated = {}

        if self.sended:
            response = self.prepare_request("/transactions/sended/validated",
                                            type="get")
            transactions_sended = response.json()

        if self.sended_not_validated:
            response = self.prepare_request(
                "/transactions/sended/not_validated", type="get")
            transactions_sended_not_validated = response.json()

        new_dict = {}

        for transaction in transactions:
            if transactions[transaction]["transaction"][
                    "signature"] in self.cache:
                continue
            else:
                if transactions[transaction]["transaction"][
                        "toUser"] == wallet_import(-1, 3):
                    new_dict[transaction] = transactions[transaction]
                    the_tx = Transaction.load_json(
                        transactions[transaction]["transaction"])

                    if not transactions[transaction]["transaction"][
                            "data"] == "NP":
                        with contextlib.suppress(json.decoder.JSONDecodeError):
                            transactions[transaction]["transaction"][
                                "data"] = json.loads(transactions[transaction]
                                                     ["transaction"]["data"])
                        if not transactions[transaction]["transaction"][
                                "data"]["app_data"].startswith("split-"):
                            self.cache.append(transactions[transaction]
                                              ["transaction"]["signature"])

                            SavetoMyTransaction(
                                the_tx) if not get_all else None
                            ValidateTransaction(
                                the_tx) if not get_all else None
                    else:
                        SavetoMyTransaction(the_tx) if not get_all else None
                        ValidateTransaction(the_tx) if not get_all else None
                        self.cache.append(transactions[transaction]
                                          ["transaction"]["signature"])
                elif transactions[transaction]["transaction"][
                        "fromUser"] == wallet_import(-1, 0):
                    transactions_sended[transaction] = transactions[
                        transaction]

        for transaction in transactions_sended:
            if self.sended:
                if (transactions_sended[transaction]["transaction"]
                    ["signature"] in self.cache):
                    continue
                else:
                    if transactions_sended[transaction]["transaction"][
                            "fromUser"] == wallet_import(-1, 0):
                        new_dict[transaction] = transactions_sended[
                            transaction]
                        the_tx = Transaction.load_json(
                            transactions_sended[transaction]["transaction"])

                        if (not transactions_sended[transaction]["transaction"]
                            ["data"] == "NP"):
                            with contextlib.suppress(
                                    json.decoder.JSONDecodeError):
                                transactions_sended[transaction][
                                    "transaction"]["data"] = json.loads(
                                        transactions_sended[transaction]
                                        ["transaction"]["data"])
                            if not transactions_sended[transaction][
                                    "transaction"]["data"][
                                        "app_data"].startswith("split-"):
                                self.cache.append(
                                    transactions_sended[transaction]
                                    ["transaction"]["signature"])

                                SavetoMyTransaction(
                                    the_tx) if not get_all else None
                                ValidateTransaction(
                                    the_tx) if not get_all else None
                        else:
                            SavetoMyTransaction(
                                the_tx) if not get_all else None
                            ValidateTransaction(
                                the_tx) if not get_all else None
                            self.cache.append(transactions_sended[transaction]
                                              ["transaction"]["signature"])
        split_not_validated = []
        for transaction in transactions_sended_not_validated:
            if self.sended_not_validated:
                if (transactions_sended_not_validated[transaction]
                    ["transaction"]["signature"] in self.cache):
                    continue
                else:
                    if transactions_sended_not_validated[transaction][
                            "transaction"]["fromUser"] == wallet_import(-1, 0):
                        the_tx = Transaction.load_json(
                            transactions_sended[transaction]["transaction"])

                        new_dict[
                            transaction] = transactions_sended_not_validated[
                                transaction]
                        if (not transactions_sended_not_validated[transaction]
                            ["transaction"]["data"] == "NP"):
                            with contextlib.suppress(
                                    json.decoder.JSONDecodeError):
                                transactions_sended_not_validated[transaction][
                                    "transaction"]["data"] = json.loads(
                                        transactions_sended_not_validated[
                                            transaction]["transaction"]
                                        ["data"])
                            if not transactions_sended_not_validated[
                                    transaction]["transaction"]["data"][
                                        "app_data"].startswith("split-"):
                                self.cache.append(
                                    transactions_sended_not_validated[
                                        transaction]["transaction"]
                                    ["signature"])

                                split_not_validated.append(
                                    transactions_sended_not_validated[
                                        transaction]["transaction"]
                                    ["signature"])
                                SavetoMyTransaction(
                                    the_tx) if not get_all else None
                        else:
                            SavetoMyTransaction(
                                the_tx) if not get_all else None
                            self.cache.append(
                                transactions_sended_not_validated[transaction]
                                ["transaction"]["signature"])

        self.save_cache()

        last_list = []

        for transaction in new_dict:
            with contextlib.suppress(TypeError):
                if not new_dict[transaction]["transaction"]["data"] == "NP":
                    if (self.app_name in new_dict[transaction]["transaction"]
                        ["data"]["action"]):
                        last_list.append(new_dict[transaction]["transaction"])

        splits = []
        # finding transactions that data start with split
        new_a_last_list = copy.copy(last_list)
        for transaction in last_list:
            # check new_dict[transaction]["transaction"]["data"] is start with split

            if transaction["data"]["app_data"].startswith("split-0"):
                the_split = splitted_data(
                    transaction["data"]["app_data"].split("-")[2])
                the_split.data_original.append(transaction)
                splits.append(the_split)
                new_a_last_list.remove(transaction) if not get_all else None

        last_list = new_a_last_list
        new_last_list = copy.copy(last_list)

        for split in splits:
            for transaction in last_list:
                if transaction["data"]["app_data"].startswith("split-"):
                    if not transaction["data"]["app_data"].startswith(
                            "split-0") and not transaction["data"][
                                "app_data"].startswith("split-1"):
                        if transaction["data"]["app_data"].split(
                                "-")[2] == split.split:
                            split.data.append(transaction["data"]["app_data"])
                            split.data_original.append(transaction)
                            new_last_list.remove(
                                transaction) if not get_all else None

        last_list = new_last_list

        new_last_list_2 = copy.copy(last_list)
        for transaction in last_list:
            finded = False

            for split in splits:
                if transaction["data"]["app_data"].startswith("split-1"):
                    if transaction["data"]["app_data"].split(
                            "-")[2] == split.split:
                        finded = True
                        split.validated = True

                        split.main_data = copy.copy(transaction)
                        split.data_original.append(copy.copy(transaction))
                        new_last_list_2.remove(
                            transaction) if not get_all else None

                        break
        last_list = new_last_list_2

        new_splits = copy.copy(splits)
        new_last_list_3 = copy.copy(last_list)
        for split in splits:
            if not split.validated:
                for each_data in split.data:
                    for transaction in last_list:
                        if each_data == transaction["data"]["app_data"]:
                            new_last_list_3.remove(
                                transaction) if not get_all else None

                            break

                new_splits.remove(split)

        last_list = new_last_list_3

        splits = new_splits

        for split in splits:
            if split.validated:
                for each_original in split.data_original:
                    self.cache.append(each_original["signature"])
                    SavetoMyTransaction(the_tx)
                    if not each_original["signature"] in split_not_validated:
                        ValidateTransaction(the_tx) if not get_all else None
                    if Address(each_original["fromUser"]) == wallet_import(
                            -1, 3):
                        SendedTransaction(Transaction.load_json(
                            each_original)) if not get_all else None
                for each_data in split.data:
                    split.main_data["data"]["app_data"] += each_data
                    split.main_data["data"]["app_data"] = split.main_data[
                        "data"]["app_data"].replace(f"split-1-{split.split}-",
                                                    "")
                    for i in range(len(split.data)):
                        split.main_data["data"]["app_data"] = split.main_data[
                            "data"]["app_data"].replace(
                                f"split-{i+2}-{split.split}-", "")
                last_list.append(split.main_data)

        self.save_cache()

        result = []

        for transaction in last_list:
            transaction["fromUser"] = Address(transaction["fromUser"])
            if transaction["fromUser"] == wallet_import(-1, 3):
                the_tx = Transaction.load_json(transaction)
                if the_settings()["baklava"] and not transaction["data"][
                        "app_data"].startswith("split-"):
                    SendedTransaction(the_tx) if not get_all else None
                result.append(transaction)

            elif transaction["toUser"] == wallet_import(-1, 3):
                result.append(transaction)

        for transaction in result[:]:
            if transaction["data"]["app_data"].startswith("split-"):
                result.remove(transaction) if not get_all else None

        if not len(result) == 0:
            logger.info("New datas received")

        return result

    def get(self, get_all=False):
        backup_host = copy.copy(self.host)
        backup_port = copy.copy(self.port)
        if the_settings()["baklava"]:
            self.host = "test_net.1.naruno.org"
            self.port = 8000

        first = []
        with contextlib.suppress(Exception):
            first = self.get_(get_all=get_all)
        self.host = backup_host
        self.port = backup_port

        second = self.get_(get_all=get_all)

        the_list = first + second

        with contextlib.suppress(TypeError):
            if "print" in inspect.stack()[1].code_context[0]:
                total = ""
                for data in the_list:
                    fromUser = data["fromUser"]
                    toUser = data["toUser"]
                    action = data["data"]["action"].replace(self.app_name, "")
                    data = data["data"]["app_data"]
                    total += f"\n-----\nFrom: {fromUser}, To: {toUser} \nApp Name: {self.app_name}, Action: {action} \nData: {data}\n-----"
                return total
        return the_list
