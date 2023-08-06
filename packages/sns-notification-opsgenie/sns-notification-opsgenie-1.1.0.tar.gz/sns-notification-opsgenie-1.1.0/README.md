# SNS Notification OpsGenie

This repository contains [AWS CDK](https://aws.amazon.com/cdk/) constructs which can be used for sns to notify to Opsgenie using [projen](https://github.com/projen/projen) + [jsii](https://github.com/aws/jsii) and publishing it to [npm](https://www.npmjs.com/) and [pypi](https://pypi.org/) repositories..

## Table of Contents

* [About projen](#about-projen)
* [About jsii](#about-jsii)
* [How to Use](#how-to-use)

## About projen

[projen](https://github.com/projen/projen) is a tool to write your project configuration using code instead of managing it yourself.projen synthesizes project configuration files such as package.json, tsconfig.json, .gitignore, GitHub Workflows, eslint, jest, etc from a well-typed definition written in JavaScript.

## About jsii

[jsii](https://aws.github.io/jsii/) allows code in any language to naturally interact with JavaScript classes. It is the technology that enables the [AWS CDK](https://aws.amazon.com/cdk/) to deliver polyglot libraries from a single codebase!

## Steps For using a `sns-notification-opsgenie` in your cdk Construct

1. Install the package based on your language:

   If you are using python, use below comand in your terminal:

   ```shell
    pip install sns-notification-opsgenie
   ```

   If you are using Typescript, use below comand in your terminal:

   ```shell
    npm i sns-notification-opsgenie
   ```
2. Next,import the package in your cdk construct based on your language:

   for Python:

   ```shell
    from sns-notification-opsgenie import SnsNotifyOpsgenie
   ```

   for Typescript:

   ```shell
    import { SnsNotifcationOpsgenie } from sns-notification-opsgenie
   ```
3. Use the method `getOpgsgenieTopicArn` by passing `AWS AcccountId`, `OpsGenie Priority` and optionally `AWS Region`. In case you do not pass any region, default region will be `eu-west-1`.
