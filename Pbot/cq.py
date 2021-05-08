def at(num) -> str:
    return f"[CQ:at,qq={num}]"


def image(path: str) -> str:
    return f"[CQ:image,file={path}]"


def link(url: str, title: str = "", content: str = "", image: str = "") -> str:
    return f"[CQ:share,url={url},title={title},content={content},image={image}]"


def reply(message_id: int):
    return f"[CQ:reply,id={message_id}]"


def xml(data: str):
    return f"[CQ:xml,data={data}]"


def music(tp: str, _id: str):
    return f"[CQ:music,type={tp},id={_id}]"


def record(file: str):
    return f"[CQ:record,file=file:///{file}]"


def js(jsstr: str):
    return f"[CQ:json,data={jsstr}]"
