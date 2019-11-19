from database import Database
import json


def main(test_flag):
    if test_flag == 0:
        build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
        extract = {"img001": ["A"], "img002": ["C1"]}
        edits = [("A1", "A"), ("A2", "A")]

    elif test_flag == 1:
        build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
        extract = {"img001": ["A", "B"], "img002": ["A", "C1"], "img003": ["B", "E"]}
        edits = [("A1", "A"), ("A2", "A"), ("C2", "C")]

    else:
        with open('./release/img_extract.json') as json_file:
            extract = json.load(json_file)
        with open('./release/graph_build.json') as json_file:
            build = json.load(json_file)
        with open('./release/graph_edits.json') as json_file:
            edits = json.load(json_file)
        with open('./release/expected_status.json') as json_file:
            expected_status = json.load(json_file)

    status = github_test_template(build, edits, extract)

    print(status)

    for key, value in status.items():
        if status[key] != expected_status[key]:
            print("key:{}, mine:{}, foodvisors:{}".format(key, status[key], expected_status[key]))


def github_test_template(build, edits, extract):
    status = {}
    if len(build) > 0:
        db = Database(build[0][0])
        if len(build) > 1:
            db.add_nodes(build[1:])
        db.add_extract(extract)
        db.add_nodes(edits)
        status = db.get_extract_status()
    return status


if __name__ == "__main__":
    main(test_flag=2)
