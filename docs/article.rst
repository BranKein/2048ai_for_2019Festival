Article api
======================





        - name: article_id
        - in: path
        - type: integer
        - description: 게시물 ID
        - required: true

        **board**

        - name: board
        - in: query
        - type: string
        - description: 수정할 게시물의 새 게시판
        - required: false

        **title**

        - name: title
        - in: query
        - type: string
        - description: 수정할 게시물의 새 제목
        - required: false

        **content**

        - name: prefix
        - in: query
        - type: string
        - description: 새 게시물의 내용물
        - required: false

        **prefix**

        - name: prefix
        - in: query
        - type: string
        - description: 수정할 게시물의 새 말머리
        - required: false

    **Example request**:

    .. sourcecode:: http

        PUT /article/1 HTTP/1.1
        Host: api.gistory.me
        Accept: application/json
        Content-Type: application/json

        {
            "board": "question",
            "title": "New Title",
            "content": "New Content",
            "prefix": "Blah"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept

    :resheader Content-Type: application/json
    :status:
        - 200: 게시물 수정 성공
        - 404: 수정하려는 게지물이 존재하지 않음

.. http:post:: /article

    **새로운 게시물 작성**

    :Paramaters:

        **board**

        - name: board
        - in: query
        - type: string
        - description: 새 게시물의 게시판 ID
        - required: true

        **title**

        - name: title
        - in: query
        - type: string
        - description: 새 게시물의 제목
        - required: true

        **content**

        - name: content
        - in: query
        - type: string
        - description: 새 게시물의 본문
        - required: true

        **prefix**

        - name: prefix
        - in: query
        - type: string
        - description: 새 게시물의 말머리
        - required: true

    **Example request**:

    .. sourcecode:: http

        POST /article HTTP/1.1
        Host: api.gistory.me
        Accept: application/json
        Content-Type: application/json

        {
            "board": "notice",
            "title": "Title",
            "content": "Content",
            "prefix": "Blah"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept

    :resheader Content-Type: application/json
    :status:
        - 200: 게시물 작성 완료
        - 404: 필요한 데이터가 오지 않음
