# -*- coding: utf-8 -*-
# This file is part of Quark-Engine - https://github.com/quark-engine/quark-engine
# See the file 'LICENSE' for copying permission.

import os

import pytest
from quark.core.struct.methodobject import MethodObject
from quark.script import (
    DefaultRuleset,
    Method,
    Ruleset,
    getActivities,
    runQuarkAnalysis,
)

RULE_FOLDER_PATH = "tests/script/rules"
RULE_FILENAME = "00068.json"
RULE_PATH = os.path.join(RULE_FOLDER_PATH, RULE_FILENAME)


@pytest.fixture(scope="class")
def QUARK_ANALYSIS_RESULT(SAMPLE_PATH_14d9f):
    ruleset = Ruleset(RULE_FOLDER_PATH)
    return runQuarkAnalysis(SAMPLE_PATH_14d9f, ruleset[RULE_FILENAME])


class TestRuleset:
    @staticmethod
    def testInitWithFolder():
        _ = Ruleset(RULE_FOLDER_PATH)

    @staticmethod
    def testGetExistentRule():
        ruleset = Ruleset(RULE_FOLDER_PATH)

        rule = ruleset[RULE_FILENAME]

        assert rule.crime == "Executes the specified string Linux command"

    @staticmethod
    def testGetNonexistentRule():
        NONEXISTENT_RULE = "NONEXISTENT_RULE.json"
        ruleset = Ruleset(RULE_FOLDER_PATH)

        with pytest.raises(KeyError):
            _ = ruleset[NONEXISTENT_RULE]


class TestDefaultRuleset:
    @staticmethod
    def testGetExistentRuleByNumber():
        ruleset = DefaultRuleset(RULE_FOLDER_PATH)

        rule = ruleset[68]

        assert rule.crime == "Executes the specified string Linux command"

    @staticmethod
    def testGetNonexistentRuleByNumber():
        ruleset = DefaultRuleset(RULE_FOLDER_PATH)

        with pytest.raises(KeyError):
            _ = ruleset[1]


class TestActivity:
    @staticmethod
    def testHasNoIntentFilter(SAMPLE_PATH_14d9f):
        activity = getActivities(SAMPLE_PATH_14d9f)[0]
        assert activity.hasIntentFilter() is False

    @staticmethod
    def testHasIntentFilter(SAMPLE_PATH_13667):
        activity = getActivities(SAMPLE_PATH_13667)[0]
        assert activity.hasIntentFilter() is True

    @staticmethod
    def testIsNotExported(SAMPLE_PATH_14d9f):
        activity = getActivities(SAMPLE_PATH_14d9f)[0]
        assert activity.isExported() is False

    @staticmethod
    def testIsExported(SAMPLE_PATH_13667):
        activity = getActivities(SAMPLE_PATH_13667)[0]
        assert activity.isExported() is True


class TestMethod:
    @staticmethod
    def testInit(QUARK_ANALYSIS_RESULT):
        methodObj = MethodObject(
            class_name="Lcom/google/progress/WifiCheckTask;",
            name="checkWifiCanOrNotConnectServer",
            descriptor="()Z",
        )

        method = Method(QUARK_ANALYSIS_RESULT, methodObj)

        assert (
            method.fullName == "Lcom/google/progress/WifiCheckTask;"
            " checkWifiCanOrNotConnectServer ()Z"
        )

    @staticmethod
    def testGetXrefTo(QUARK_ANALYSIS_RESULT):
        methodObj = QUARK_ANALYSIS_RESULT.quark.apkinfo.find_method(
            "Lcom/google/progress/WifiCheckTask;",
            "checkWifiCanOrNotConnectServer",
            "()Z",
        )
        method = Method(QUARK_ANALYSIS_RESULT, methodObj)

        expectedMethod = Method(
            QUARK_ANALYSIS_RESULT,
            MethodObject(
                "Landroid/util/Log;",
                "e",
                "(Ljava/lang/String; Ljava/lang/String;)I",
            ),
        )
        expectedOffset = 116

        callee_list = method.getXrefTo()

        assert (expectedMethod, expectedOffset) in callee_list

    @staticmethod
    def testGetXrefFrom(QUARK_ANALYSIS_RESULT):
        methodObj = QUARK_ANALYSIS_RESULT.quark.apkinfo.find_method(
            "Lcom/google/progress/WifiCheckTask;",
            "checkWifiCanOrNotConnectServer",
            "([Ljava/lang/String;)Z",
        )
        method = Method(QUARK_ANALYSIS_RESULT, methodObj)

        expectedMethod = Method(
            QUARK_ANALYSIS_RESULT,
            MethodObject("Lcom/google/progress/WifiCheckTask;", "test", "()V"),
        )

        caller_list = method.getXrefFrom()

        assert expectedMethod in caller_list


class TestBehavior:
    @staticmethod
    def testHasString(QUARK_ANALYSIS_RESULT):
        behaviorOccurList = QUARK_ANALYSIS_RESULT.behaviorOccurList
        behavior = next(
            filter(
                lambda b: "checkWifiCanOrNotConnectServer"
                in b.methodCaller.fullName,
                behaviorOccurList,
            )
        )

        result = behavior.hasString("ping")

        assert result

    @staticmethod
    def testHasUrl(QUARK_ANALYSIS_RESULT):
        behaviorOccurList = QUARK_ANALYSIS_RESULT.behaviorOccurList
        behavior = next(
            filter(
                lambda b: "checkWifiCanOrNotConnectServer"
                in b.methodCaller.fullName,
                behaviorOccurList,
            )
        )

        result = behavior.hasUrl()

        assert "www.baidu.com" in result

    @staticmethod
    def testGetParamValues(QUARK_ANALYSIS_RESULT):
        behaviorOccurList = QUARK_ANALYSIS_RESULT.behaviorOccurList
        behavior = next(
            filter(
                lambda b: "checkWifiCanOrNotConnectServer"
                in b.methodCaller.fullName,
                behaviorOccurList,
            )
        )

        assert behavior.getParamValues()[0] == "ping www.baidu.com"


class TestQuarkReuslt:
    @staticmethod
    def testMethodGetXrefTo(QUARK_ANALYSIS_RESULT):
        methodObj = QUARK_ANALYSIS_RESULT.quark.apkinfo.find_method(
            "Lcom/google/progress/WifiCheckTask;",
            "checkWifiCanOrNotConnectServer",
            "()Z",
        )
        method = Method(QUARK_ANALYSIS_RESULT, methodObj)

        expectedMethod = Method(
            QUARK_ANALYSIS_RESULT,
            MethodObject(
                "Landroid/util/Log;",
                "e",
                "(Ljava/lang/String; Ljava/lang/String;)I",
            ),
        )
        expectedOffset = 116

        callee_list = QUARK_ANALYSIS_RESULT.getMethodXrefTo(method)

        assert (expectedMethod, expectedOffset) in callee_list

    @staticmethod
    def testMethodGetXrefFrom(QUARK_ANALYSIS_RESULT):
        methodObj = QUARK_ANALYSIS_RESULT.quark.apkinfo.find_method(
            "Lcom/google/progress/WifiCheckTask;",
            "checkWifiCanOrNotConnectServer",
            "([Ljava/lang/String;)Z",
        )
        method = Method(QUARK_ANALYSIS_RESULT, methodObj)

        expectedMethod = Method(
            QUARK_ANALYSIS_RESULT,
            MethodObject("Lcom/google/progress/WifiCheckTask;", "test", "()V"),
        )

        caller_list = QUARK_ANALYSIS_RESULT.getMethodXrefFrom(method)

        assert expectedMethod in caller_list

    @staticmethod
    def testgetAllStrings(QUARK_ANALYSIS_RESULT):
        assert len(QUARK_ANALYSIS_RESULT.getAllStrings()) == 1005

    @staticmethod
    def testfindMethodInCaller(QUARK_ANALYSIS_RESULT):
        callerMethod = [
            "Lcom/google/progress/WifiCheckTask;",
            "checkWifiCanOrNotConnectServer",
            "([Ljava/lang/String;)Z",
        ]
        targetMethod = [
            "Landroid/util/Log;",
            "e",
            "(Ljava/lang/String; Ljava/lang/String;)I",
        ]

        assert QUARK_ANALYSIS_RESULT.findMethodInCaller(
            callerMethod, targetMethod
        )


def testRunQuarkAnalysis(SAMPLE_PATH_14d9f):
    ruleset = Ruleset(RULE_FOLDER_PATH)
    ruleObj = ruleset[RULE_FILENAME]

    analysisResult = runQuarkAnalysis(SAMPLE_PATH_14d9f, ruleObj)

    assert len(analysisResult.behaviorOccurList) == 1


def testGetActivities(SAMPLE_PATH_14d9f) -> None:
    activities = getActivities(SAMPLE_PATH_14d9f)

    assert len(activities) == 1
    assert str(activities[0]) == "com.google.progress.BackGroundActivity"
