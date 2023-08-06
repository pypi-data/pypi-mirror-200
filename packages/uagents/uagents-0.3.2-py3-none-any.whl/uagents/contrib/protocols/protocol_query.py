from typing import Any, Dict, List, Optional

from uagents import Context, Model, Protocol


class ProtocolQuery(Model):
    protocol_schema_digest: Optional[str]


class ProtocolResponse(Model):
    protocols: List[Dict[str, Any]]


proto_query = Protocol()


@proto_query.on_query(ProtocolQuery)
async def send_protocol_message_schemas(ctx: Context, sender: str, msg: ProtocolQuery):
    if msg.protocol_schema_digest is not None:
        if msg.protocol_schema_digest in ctx.protocols:
            protocols = [ctx.protocols[msg.protocol_schema_digest]]
    else:
        protocols = list(ctx.protocols.values())

    all_proto_infos = []
    for protocol in protocols:
        proto_msgs = set()
        proto_msgs = proto_msgs.union(set(protocol.models.values()))
        proto_replies = {}
        for msg, replies in protocol.replies.items():
            for reply in replies.values():
                proto_msgs.add(reply)

        proto_msg_schemas = [message.schema() for message in proto_msgs]
        proto_info = {
            "name": protocol.name,
            "version": protocol.version,
            "digest": protocol.digest,
            "messages": proto_msg_schemas,
        }
        all_proto_infos.append(proto_info)

    await ctx.send(sender, ProtocolResponse(protocols=all_proto_infos))
