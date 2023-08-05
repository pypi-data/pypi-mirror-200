from dataclasses import dataclass, field

@dataclass
class Esm1bConfig:
    num_layers: int = field(
        default=33,
        metadata={"help": ""},
    )
    embed_dim: int = field(
        default=1280,
        metadata={"help": ""},
    )
    logit_bias: bool = field(
        default=True,
        metadata={"help": ""},
    )
    ffn_embed_dim: int = field(
        default=5120,
        metadata={"help": ""},
    )
    attention_heads: int = field(
        default=20,
        metadata={"help": ""},
    )
    max_positions: int = field(
        default=1024,
        metadata={"help": ""},
    )
    emb_layer_norm_before: bool = field(
        default=True,
        metadata={"help": ""},
    )
    checkpoint_path: str = field(
        default=None,
        metadata={"help": ""},
    )