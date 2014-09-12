# Atheme IRC Services の設定

./doc/rpmbuild.md でインストールした Atheme IRC Services に、IRCサーバーとリレーさせるための設定を施していきます。

前提として、IRCサーバーは同一ホストですでに稼働中とします。  
使っているIRCサーバーは、 yum でインストールした ngIRCd です。パッケージ名 "ngircd-21-1.el6.x86_64" 


## IRCサーバー側の設定

Atheme IRC Services は、IRCサーバーのようにふるまいます。つまり、IRCクライアント(ボット)として稼働するわけではないということです。  
IRCサーバー側で、サーバーリレーの設定をしないと使えません。

例えば以下のようにIRCサーバーの設定を書き加え、 reload して読み込ませます。

```
[Server]
        Name = atheme.kazagakure.net
        Host = 127.0.0.1
        Port = 6663
        PeerPassword = パスワード1
        MyPassword = パスワード2
        Passive = yes
        ServiceMask = *Serv,Global
```


## Atheme IRC Services の設定

まず最初に、用意されている設定ファイルのテンプレートをコピーします。

```
# cp /etc/atheme/atheme.conf.example /etc/atheme/atheme.conf
```

このコピーしたファイル(/etc/atheme/atheme.conf)を編集していきます。  
詳細なコメントが書かれたかなり長い(2000行を超えるくらい?)ファイルです。

書式はC/C++言語と同じスタイル。  
/* */と半角シャープでコメントに、行末には半角セミコロンが必要です。


### リレーするサーバープログラムの指定

"Protocol module"というのが、リレーするIRCサーバーによって変わる部分になります。  
「loadmodule "modules/protocol/xxxxxx";」という行を探して、使うIRCサーバーにあった設定に変えます。

```
loadmodule "modules/protocol/ngircd";
```

最初からある程度 NickServ や ChanServ などが有効化されていますので、このあたりのモジュール読み込み設定の部分は素っ飛ばします。  
それぞれのコマンドがほぼ一つずつモジュールになっていて、個別に有効化・無効化が切り換えられるようになっているようです。


### サービスの見え方の設定

serverinfo{} という部分にまとまっています。

* name  
普通のIRCサーバーやIRCクライアントから、ネットワークを構成するリレーサーバーとして Atheme IRC Services が扱われるときの、サーバー名を指定します。
* desc  
name と同じく、サーバーの説明を指定します。
* netname  
IRCリレーネットワークの名前を指定します。  
メールで登録情報やパスワードリセットコードを送るときにも使われます。
* adminname / adminemail  
管理者の名前とメールアドレスを指定します。
* registeremail  
登録時やパスワードリセット時などにメールを送ります。その時の差出人アドレス(Fromに書かれるアドレス)を指定します。
* mta  
メールを送るときに使うコマンドを指定します。  
Postfix の場合は、デフォルトの sendmail コマンドを使うと発信日が UNIX エポック時になってしまったので、 /bin/mail に変更しました。


### サーバーリレーの設定

uplink というところで設定します。

* uplink "irc.example.net"  
リレーするIRCサーバーの名前を指定します。
* host  
リレーするIRCサーバーのホスト名(もしくはIPアドレス)を入力します。
* send_password  
IRCサーバーのほうで指定した「パスワード2」を指定します。
* receive_password  
同様に、「パスワード1」を指定します。
* port  
IRCサーバーとリレーするときにつかうポートを指定します。

標準では IPv4/IPv6 2つのサーバー設定が用意されています。不要な方はコメントアウトして無効化します。


## Atheme IRC Services の起動

では、起動してみます。

システムにサービスとして登録した場合(SysVinitに登録した場合)は、ほかのデーモンと同じように service コマンドや、シェルスクリプトを起動します。

そうでない場合は /usr/bin/atheme-services を起動します。  
オプションなどを適切に指定しないと設定ファイルを読み込んでくれません。

```
# service atheme-services start
Atheme IRC Services を起動中: [12/09/2014 21:38:31] atheme 7.1.0 is starting up...
[12/09/2014 21:38:31] module_load(): module /usr/lib64/atheme/modules/groupserv/main is already loaded [at 0x13990d0]
[12/09/2014 21:38:31] opensex: grammar version is 1.
[12/09/2014 21:38:31] corestorage: data schema version is 12.
[12/09/2014 21:38:31] groupserv: opensex data schema version is 4.
[12/09/2014 21:38:31] pid 52736
[12/09/2014 21:38:31] running in background mode from /usr
                                                           [  OK  ]
```

最初はフォアグラウンドモードで起動し、余計なモジュールが有効化されていないか、設定は間違っていないかを確認する方がいいかもしれません。

```
# /usr/bin/atheme-services -h
usage: atheme [-dhnvr] [-c conf] [-l logfile] [-p pidfile]

-c <file>    Specify the config file
-d           Start in debugging mode
-h           Print this message and exit
-r           Start in read-only mode
-l <file>    Specify the log file
-n           Don't fork into the background (log screen + log file)
-p <file>    Specify the pid file (will be overwritten)
-D <dir>     Specify the data directory
-v           Print version information and exit
# /usr/bin/atheme-services -c /etc/atheme/atheme.conf -n
```

IRCサーバーとリレーされたら、インストールは完了です。  
試しに NickServ のヘルプを出力させてみましょう。

```
$ telnet localhost 6663
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.

nick koi-telnet
user koi-chan 0 0 ::

:irc.kazagakure.net 001 koi-telnet :Welcome to the Internet Relay Network koi-telnet!~koi-chan@localhost
(省略)
:irc.kazagakure.net 376 koi-telnet :End of MOTD command
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :Welcome to KAZAGAKURE in Creator's Network IRC, koi-telnet! Here on KAZAGAKURE in Creator's Network IRC, we provide services to enable the registration of nicknames and channels! For details, type /msg NickServ help and /msg ChanServ help.

privmsg NickServ help

:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :***** NickServ Help *****
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :NickServ allows users to 'register' a nickname, and stop
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :others from using that nick. NickServ allows the owner of a
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :nickname to disconnect a user from the network that is using
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :their nickname.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :If a registered nick is not used by the owner for 30 days,
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :NickServ will drop the nickname, allowing it to be reregistered.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :For more information on a command, type:
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :/msg NickServ help <command>
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :For a verbose listing of all commands, type:
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :/msg NickServ help commands
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :The following commands are available:
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :GHOST           Reclaims use of a nickname.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :IDENTIFY        Identifies to services for a nickname.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :INFO            Displays information on registrations.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :LISTCHANS       Lists channels that you have access to.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :REGISTER        Registers a nickname.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :SENDPASS        Email registration passwords.
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :Other commands: ACC, DROP, HELP, LISTGROUPS, LOGOUT, SETPASS,
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :                STATUS, TAXONOMY, VERIFY
:NickServ!NickServ@atheme.kazagakure.net NOTICE koi-telnet :***** End of Help *****

quit

:irc.kazagakure.net NOTICE koi-telnet :Connection statistics: client 0.1 kb, server 9.4 kb.
ERROR :Closing connection
Connection closed by foreign host.
```

上の例では、Telnet を使って実験してみました。  
うまく動いているようですね。
