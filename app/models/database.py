from typing import Optional

from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, BigInteger, DateTime


def utc_now():
    return datetime.now(timezone.utc)


class WilayahKecamatan(SQLModel, table=True):
    __tablename__ = "wilayah_kecamatan"

    id_kecamatan: int = Field(primary_key=True)
    nama_kecamatan: str

    desas: list["WilayahDesa"] = Relationship(back_populates="kecamatan")


class WilayahDesa(SQLModel, table=True):
    __tablename__ = "wilayah_desa"

    id_desa: int = Field(sa_column=Column(BigInteger, primary_key=True))
    kecamatan_id: int = Field(foreign_key="wilayah_kecamatan.id_kecamatan")
    nama_desa: str

    kecamatan: WilayahKecamatan = Relationship(back_populates="desas")


class TikTokUser(SQLModel, table=True):
    __tablename__ = "tiktok_user"

    id_tiktok_user: str = Field(primary_key=True)
    username: str
    avatar_thumbnail: str | None = None
    is_priority: bool = Field(default=False)

    created_at: datetime | None = Field(
        default_factory=utc_now, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), onupdate=utc_now),
    )

    videos: list["TikTokVideo"] = Relationship(back_populates="tiktok_user")
    comments: list["TikTokComment"] = Relationship(back_populates="user")

    opd: Optional["OrganisasiPerangkatDaerah"] = Relationship(
        back_populates="tiktok_user"
    )


class OrganisasiPerangkatDaerah(SQLModel, table=True):
    __tablename__ = "organisasi_perangkat_daerah"

    id_opd: int = Field(primary_key=True)
    nama_opd: str
    singkatan: str | None = None
    deskripsi_tugas: str | None = None
    kategori_tugas: str | None = None

    tiktok_user_id: str | None = Field(
        default=None, foreign_key="tiktok_user.id_tiktok_user"
    )

    created_at: datetime | None = Field(
        default_factory=utc_now, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), onupdate=utc_now),
    )
    deleted_at: datetime | None = Field(default=None)

    tiktok_user: Optional[TikTokUser] = Relationship(back_populates="opd")


class TikTokVideo(SQLModel, table=True):
    __tablename__ = "tiktok_video"

    id_tiktok_video: str = Field(primary_key=True)
    tiktok_user_id: str = Field(foreign_key="tiktok_user.id_tiktok_user")
    video_web_url: str
    submitted_video_url: str
    video_created_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    created_at: datetime | None = Field(
        default_factory=utc_now, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), onupdate=utc_now),
    )

    tiktok_user: TikTokUser = Relationship(back_populates="videos")
    comments: list["TikTokComment"] = Relationship(back_populates="video")


class TikTokComment(SQLModel, table=True):
    __tablename__ = "tiktok_comment"

    id_tiktok_comment: str = Field(primary_key=True)
    video_id: str = Field(foreign_key="tiktok_video.id_tiktok_video")
    user_id: str = Field(foreign_key="tiktok_user.id_tiktok_user")

    input_url: str
    create_time: int
    create_time_iso: datetime
    text: str
    digg_count: int
    liked_by_author: bool
    pinned_by_author: bool

    replies_to_id: str | None = Field(
        default=None, foreign_key="tiktok_comment.id_tiktok_comment"
    )
    reply_comment_total: int

    created_at: datetime | None = Field(
        default_factory=utc_now, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), onupdate=utc_now),
    )
    deleted_at: datetime | None = Field(default=None)

    video: TikTokVideo = Relationship(back_populates="comments")
    user: TikTokUser = Relationship(back_populates="comments")

    parent_comment: Optional["TikTokComment"] = Relationship(
        back_populates="replies",
        sa_relationship_kwargs={"remote_side": "TikTokComment.id_tiktok_comment"},
    )
    replies: list["TikTokComment"] = Relationship(back_populates="parent_comment")
