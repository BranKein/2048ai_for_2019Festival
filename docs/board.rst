Board api
===============

.. http:get:: /board/(string:board_id)

    **게시판의 글 목록을 반환함**

    :Paramaters:

        **board_id**

        - name: board_id
        - in: path
        - type: string
        - description: 게시판 ID
        - required: true

        **start_idx**

        - name: start_idx
        - in: query
        - type: integer
        - default: 0
        - description: 가져올 글의 [start_idx, end_idx] 중 start_idx.
        - required: false

        **end_idx**

        - name: end_idx
        - in: query
        - type: integer
        - default: 20
        - description: 가져올 글의 [start_idx, end_idx] 중 end_idx.
        - required: false

        **sort_type**

        - name: sort_type
        - in: query
        - type: string
        - default: id_desc
        - description

            - 정렬 방식, 아래 methods를 사용할 수 있음
            - id_asc
            - id_desc
            - title_asc
            - title_desc
            - views_asc
            - views_desc
            - reg_date_asc
            - reg_date_desc
            - last_modified_asc
            - last_modified_desc
        - required: false

        **include_notifications**

        - name: include_notifications
        - in: query
        - type: boolean
        - default: true
        - description: 공지를 포함할 지 유무. 포함 시 모든 request에 공지가 포함되며, 공지 전체 + (end_idx - start_idx) 길이의 article list가 반환됨.
        - required: false

    **Example request**:

    .. sourcecode:: http

        GET /board/question HTTP/1.1
        Host: api.gistory.me
        Accept: application/json
        Content-Type: application/json

            {
                "start_idx": 3,
                "end_idx": 5,
                "include_notification": false
            }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

            [
                {
                    "id": 7,
                    "is_notify": 0,
                    "last_modified": "Sat, 22 Aug 2020 04:21:33 GMT",
                    "reg_date": "Mon, 17 Aug 2020 01:59:48 GMT",
                    "prefix": "Blah",
                    "submitter": "7493683866F544D5907E93637D6B65A3",
                    "title": "질문게시판 테스트제목3",
                    "views": 0
                },
                {
                    "id": 8,
                    "is_notify": 0,
                    "last_modified": "Sat, 22 Aug 2020 04:21:33 GMT",
                    "reg_date": "Mon, 17 Aug 2020 01:59:55 GMT",
                    "prefix": "Blah",
                    "submitter": "7493683866F544D5907E93637D6B65A3",
                    "title": "질문게시판 테스트제목4",
                    "views": 0
                },
                {
                    "id": 21,
                    "is_notify": 0,
                    "last_modified": "Sat, 22 Aug 2020 04:21:33 GMT",
                    "reg_date": "Fri, 21 Aug 2020 20:13:46 GMT",
                    "prefix": "Blah",
                    "submitter": "7493683866F544D5907E93637D6B65A3",
                    "title": "ㅇㄷㅇㄷㅇㄷ",
                    "views": 0
                }
            ]

:resheader Content-Type: application/json
:status:
    - 200: 성공적으로 요청을 수행함
    - default: 요청이 수행되지 않음
:returns: Article 리스트
