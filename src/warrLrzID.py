"""userncquota.py - FreeIPA plugin to set a quota for nextcloud users.

Copyright (C) $( 2020 ) Radio Bern RaBe
                        Switzerland
                        http://www.rabe.ch

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU Affero General Public
License as published  by the Free Software Foundation, version
3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License  along with this program.
If not, see <http://www.gnu.org/licenses/>.

Please submit enhancements, bugfixes or comments via:
https://github.com/radiorabe/kanboard-tasks-from-email

Authors:
 Simon Nussbaum <smirta@gmx.net>


For this to work, extending the LDAP schema is required.

Installation:
Copy file to <path to python lib>/ipaserver/plugins/

Usage:
ipa user-mod --lrzID="ab123xy" <username>
"""

from ipaserver.plugins import user
from ipalib.parameters import Str
from ipalib.text import _

user.user.takes_params = user.user.takes_params + (
    Str(
        "warrLrzID?",
        cli_name="warrLrzID",
        label=_("LRZ user ID"),
        doc=_(
            'LRZ user ID (e.g. "ab123xy")'
        ),
        default="none",
        autofill=False,
        pattern="^(default|none|[0-9]+ [MGT]B)$",
        pattern_errmsg="".join(
            'may only be "none", '
            '"default" or a number of mega-, giga- or terabytes (e.g. 1024 MB)'
        ),
    ),
)

user.user.default_attributes.append("warrLrzID")


# pylint: disable-msg=unused-argument,invalid-name,line-too-long
def useradd_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    """Callback for `register_pre_callback`.

    See <https://github.com/freeipa/freeipa/blob/master/doc/guide/guide.org#extending-existing-object> for details.
    """
    entry["objectclass"].append("tumUser")
    return dn


user.user_add.register_pre_callback(useradd_precallback)


# pylint: disable-msg=unused-argument,invalid-name,line-too-long
def usermod_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    """Callback for `register_pre_callback`.

    See <https://github.com/freeipa/freeipa/blob/master/doc/guide/guide.org#extending-existing-object> for details.
    """
    if "objectclass" not in entry.keys():
        old_entry = ldap.get_entry(dn, ["objectclass"])
        entry["objectclass"] = old_entry["objectclass"]
    entry["objectclass"].append("tumUser")
    return dn


user.user_mod.register_pre_callback(usermod_precallback)
