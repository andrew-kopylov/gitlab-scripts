
# pip install python-gitlab
import gitlab

oauth_token = "..."
group_name = "group-name"
include_users = []
exclude_users = []


def main():

    gl = gitlab.Gitlab(oauth_token=oauth_token)
    gl_group = gl.groups.get(group_name)
    print_users(gl_group)

    # All subgroups
    subgroup_list = gl_group.descendant_groups.list(all=True)
    for sg in subgroup_list:
        subgroup = gl.groups.get(id=sg.get_id())
        print_users(subgroup)

    # All projects
    project_list = gl_group.projects.list(all=True, include_subgroups=True)
    for gp in project_list:
        project = gl.projects.get(id=gp.get_id())
        print_users(project)


def print_users(owner):
    users = users_list(owner)
    if len(users) > 0:
        print(f"{owner.web_url}")
        for user_name in users:
            print(f"- {user_name}")


def users_list(owner) -> list:
    users = []
    members_list = owner.members.list()
    for member in members_list:
        if len(include_users) > 0:
            if member.username in include_users:
                users.append(member.username)
        elif member.username not in exclude_users:
            users.append(member.username)
    return users


if __name__ == "__main__":
    main()
