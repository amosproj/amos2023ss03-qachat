# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Felix Nützel

import os


def get_tokens_path():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return script_dir + "/tokens.env"
