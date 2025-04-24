#!/bin/bash

# ### const value Start ###
WARNING="WARNING:"
ERROR="ERROR:"
# ### const value  End  ###


# venv 作成パス
VENVPATH="`cd $(dirname ${0}) && pwd`/.venv"
# venv スクリプトパス
SCRIPTSPATH="$VENVPATH/bin"

echo "###  Start Setup.  ###"

# venv が作成されていれば venv は作成しない
echo -n "create venv ... "
if [ ! -e $VENVPATH ]; then
    if [ "$(uname)" == "Darwin" ]; then
        python3 -m venv $VENVPATH
    elif [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; then
        python -m venv $VENVPATH
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        python3 -m venv $VENVPATH
    else
        "Unknown OS"
        exit 0
    fi
    echo "ok"
else
    echo "ok"
    echo "$WARNING Already exist venv! Please remove $VENVPATH if you want to clean setup."
fi

# venv を有効化
if [ "$(uname)" == "Darwin" ]; then
    source "$VENVPATH/bin/activate"
elif [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; then
    . "$VENVPATH/Scripts/activate"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    source "$VENVPATH/bin/activate"
fi

echo -n "install library ... "
# ライブラリインストール
pip --disable-pip-version-check --quiet install -r "`cd $(dirname ${0}) && pwd`/requirements.txt"
echo "ok"

echo -e
# インストール後の環境
pip --disable-pip-version-check list

# venv を非アクティブ化
if [ "$(uname)" == "Darwin" ]; then
    source "$VENVPATH/bin/deactivate"
elif [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; then
    deactivate
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    source "$VENVPATH/bin/deactivate"
fi

echo -e 
echo "###  Finished Setup.  ###"
exit 0