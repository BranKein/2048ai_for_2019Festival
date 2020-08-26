Comment api
======================

.. http:get:: /article/(int:article_id)/comment

    **게시물에 있는 답글들을 반환함**

    :Paramaters:

        **article_id**

        - name: article_id
        - in: path
        - type: integer
        - description: 게시물 ID
        - required: true


    **Example request**:

    .. sourcecode:: http

        GET /article/(int:article_id)/comment HTTP/1.1
        Host: api.gistory.me
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

            { // Not Yet
                "board": "notice",
                "content": "testbody",
                "id": 1,
                "is_notify": 0,
                "is_visible": 1,
                "last_modified": "Sat, 22 Aug 2020 04:21:33 GMT",
                "reg_date": "Fri, 14 Aug 2020 00:06:35 GMT",
                "submitter": "7493683866F544D5907E93637D6B65A3",
                "title": "testarticle",
                "views": 0
            }

    :resheader Content-Type: application/json
    :status:
        - 404: 가져오려는 답글이 존재하지 않음
    :returns: information of article


.. http:delete:: /article/(int:article_id)/(int:comment_id)

    **답글 삭제**

    :Paramaters:

        **article_id**

        - name: article_id
        - in: path
        - type: integer
        - description: 게시물 ID
        - required: true

        **comment_id**

        - name: comment_id
        - in: path
        - type: integer
        - description: 댓글 ID
        - required: true

    **Example request**:

    .. sourcecode:: http

        DELETE /comment/(int:article_id)/(int:comment_id) HTTP/1.1
        Host: api.gistory.me
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept

    :resheader Content-Type: application/json
    :status:
        - 404: 삭제하려는 답글이 존재하지 않음
        - 500: 알 수 없는 오류 발생


.. http:put:: /article/(int:article_id)/(int:comment_id)

    **답글 수정**

    :Paramaters:

        **article_id**

        - name: article_id
        - in: path
        - type: integer
        - description: 게시물 ID
        - required: true

        **comment_id**

        - name: comment_id
        - in: path
        - type: integer
        - description: 댓글 ID
        - required: true

        **content**

        - name: content
        - in: query
        - type: string
        - description: 수정할 게시물의 새 본문
        - required: false

        **is_secret**

        - name: is_secret
        - in: query
        - type: boolean
        - description: 수정할 게시물의 secret 여부
        - required: false

        **is_visible**

        - name: is_visible
        - in: query
        - type: boolean
        - description: 수정할 게시물의 visible 여부
        - required: false

    **Example request**:

    .. sourcecode:: http

        PUT /article/(int:article_id)/(int:comment_id) HTTP/1.1
        Host: api.gistory.me
        Accept: application/json
        Content-Type: application/json

            {
                "content": "New content",
                "is_secret": False,
                "is_visible": True
            }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept

    :resheader Content-Type: application/json
    :status:
        - 200: 답글 수정 정상 완료
        - 404: 수정할 답글이 존재하지 않음
        - 500: 알 수 없는 오류 발생

.. http:post:: /article/(int:article_id)/comment

    **새로운 답글 작성**

    :Paramaters:

        **article_id**

        - name: article_id
        - in: path
        - type: integer
        - description: 답글을 달 게시물의 ID
        - required: true

        **content**

        - name: content
        - in: query
        - type: string
        - description: 답글의 본문
        - required: true

        **is_secret**

        - name: is_secret
        - in: query
        - type: boolean
        - description: 답글의 secret 여부
        - required: true

    **Example request**:

    .. sourcecode:: http

        POST /comment/0 HTTP/1.1
        Host: api.gistory.me
        Content-Type: application/json

            {
                "content": "content",
                "is_secret": False
            }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept

    :resheader Content-Type: application/json
    :status:
        - 200: 답글 작성 성공
        - 400: 필요한 데이터가 오지 않음
        - 500: 알 수 없는 오류 발생
