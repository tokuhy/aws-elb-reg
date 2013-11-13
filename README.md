aws-elb-reg
===========

Description
-----------
When the EC2 instance start/stop, run the registration/deregistration to ELB
automatically based on the tag information of an instance.
For the RHEL6 and its clone OS.
It may be able to work if you change the setting and location of the script
corresponding to the other OS (not supported).

--

EC2インスタンスの起動・停止時に、インスタンスの特定のタグ情報に基いて、
ELBに対して登録と解除を自動で実行します。
RHEL6 とそのクローンOS が対象です。
その他の OS への対応はスクリプトの配置場所や設定を変更すれば対応できるかもしれません（未対応）。

Install & Usage
---------------
Python 2.6 (or later) and Boto module is required.
Please install rpm package  or pip the boto module.

aws-elb-reg to install the rpm package in the case of CentOS6 and RHEL6.

    # rpm -ivh aws-elb-reg-<version>.rpm

After installation, you edit the /etc/sysconfig/aws-elb-reg.
Next, set the  access key, secret key and ELB configuration information tag name of EC2 instance.
You can specify the ELB name of more than one delimiter ',' in the tag.

Add to ELB

    # service aws-elb-reg {start|add}

Delete from ELB

    # service aws-elb-reg {stop|delete}

Check registration (Detect ELB that is actually registered in.)

    # service aws-elb-reg status

--

動作には Python 2.6 以上 と boto モジュールが必要です。
boto モジュールは pip もしくは パッケージで別途インストールしてください。

aws-elb-reg は RHEL6 や CentOS6 の場合は rpm パッケージでインストールします。

    # rpm -ivh aws-elb-reg-<version>.rpm

インストール後に /etc/sysconfig/aws-elb-reg ファイルを編集します。
アクセスキーとシークレットキー、インスタンスの ELB 設定情報タグ名設定します。
インスタンスのタグでは ',' 区切りで複数のELB名を指定可能です。

設定後、 service コマンドで ELB への登録・解除・ステータス確認が行えます。

ELBへ追加

    # service aws-elb-reg <start|add>

ELBから削除

    # service aws-elb-reg <stop|delete>

ELBへの登録状況確認（タグの値ではなく実際に登録されているELBを検出）

    # service aws-elb-reg status

Author
------
Fumiaki Tokuyama (tokuhy _at_ gmail.com)

Copyright & License
-------------------
    Copyright 2013 Fumiaki Tokuyama
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
      http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


