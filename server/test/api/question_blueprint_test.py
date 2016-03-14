from server.library.util import find
from server.test import assert_api_error, assert_api_response, assert_api_success

def test_question_get(auth_client, paper_with_course_and_questions):
    paper = paper_with_course_and_questions
    question = paper.questions[0]

    resp = auth_client.get("/course/{code}/paper/{year}/{period}/q/{question}".format(
        code=paper.course.code.lower(), 
        year=paper.year_start,
        period=paper.period.lower(),
        question=".".join(map(str, question.path))
    ))

    with assert_api_response(resp) as data:
        assert "question" in data
        assert "children" in data

def test_question_update(auth_client, session, paper_with_course_and_questions):
    paper = paper_with_course_and_questions
    question = paper.questions[0]

    resp = auth_client.put("/course/{code}/paper/{year}/{period}/q/{question}".format(
        code=paper.course.code.lower(), 
        year=paper.year_start,
        period=paper.period.lower(),
        question=".".join(map(str, question.path))
    ), data={
        "content": "Hello world!",
        "marks": 1238
    })

    with assert_api_response(resp) as data:
        session.refresh(question)
        assert question.revision.content == "Hello world!"
        assert len(question.revisions) > 0
        assert question.marks == 1238

def test_question_create_error_without_index(auth_client, session, course_with_papers):
    course = course_with_papers
    paper = course.papers[0]

    resp = auth_client.post("/course/{code}/paper/{year}/{period}/q/".format(
        code=paper.course.code.lower(), 
        year=paper.year_start,
        period=paper.period.lower()
    ), data={
        "index_type": "alpha",
        "content": "Hello world"
    })

    assert_api_error(resp, 422)

def test_question_create(auth_client, session, course_with_papers):
    course = course_with_papers
    paper = course.papers[0]

    resp = auth_client.post("/course/{code}/paper/{year}/{period}/q/".format(
        code=paper.course.code.lower(), 
        year=paper.year_start,
        period=paper.period.lower()
    ), data={
        "index": 1,
        "index_type": "alpha",
        "content": "Hello world"
    })

    with assert_api_response(resp) as data:
        assert "question" in data
        question_data = data["question"]
        assert "id" in question_data
        assert "revision" in question_data
        revision_data = question_data["revision"]
        assert revision_data["content"] == "Hello world"

def test_question_create_as_child(auth_client, session, paper_with_course_and_questions):
    paper = paper_with_course_and_questions
    course = paper.course
    question = paper.questions[0]

    resp = auth_client.post("/course/{code}/paper/{year}/{period}/q/{question}".format(
        code=paper.course.code.lower(), 
        year=paper.year_start,
        period=paper.period.lower(),
        question=".".join(map(str, question.path))
    ), data={
        "index": 4,
        "index_type": "alpha",
        "content": "Hello world"
    })

    with assert_api_response(resp) as data:
        assert "question" in data
        question_data = data["question"]
        assert "id" in question_data
        assert "revision" in question_data
        revision_data = question_data["revision"]
        assert revision_data["content"] == "Hello world"

        session.refresh(question)
        assert find(question.children, lambda q: q.id == question_data["id"])

def test_question_create_as_child_error_index_type(auth_client, session, paper_with_course_and_questions):
    paper = paper_with_course_and_questions
    course = paper.course
    question = paper.questions[0]

    resp = auth_client.post("/course/{code}/paper/{year}/{period}/q/{question}".format(
        code=paper.course.code.lower(), 
        year=paper.year_start,
        period=paper.period.lower(),
        question=".".join(map(str, question.path))
    ), data={
        "index": 4,
        "index_type": "decimal",
        "content": "Hello world"
    })

    assert_api_error(resp, 400)

def test_question_create_as_child_error_path_exists(auth_client, session, paper_with_course_and_questions):
    paper = paper_with_course_and_questions
    course = paper.course
    question = paper.questions[0]

    resp = auth_client.post("/course/{code}/paper/{year}/{period}/q/{question}".format(
        code=paper.course.code.lower(), 
        year=paper.year_start,
        period=paper.period.lower(),
        question=".".join(map(str, question.path))
    ), data={
        "index": 1,
        "index_type": "alpha",
        "content": "Hello world"
    })

    assert_api_error(resp, 409)