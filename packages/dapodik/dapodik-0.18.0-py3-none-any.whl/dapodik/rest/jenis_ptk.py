import attr
from datetime import datetime
from typing import Optional


@attr.dataclass(frozen=True, slots=True)
class JenisPtk:
    jenis_ptk_id: int
    jenis_ptk: str
    guru_kelas: str
    guru_matpel: str
    guru_bk: str
    guru_inklusi: str
    guru_pengganti: str
    pengawas_satdik: str
    pengawas_plb: str
    pengawas_matpel: str
    pengawas_bidang: str
    tas: str
    tendik_lainnya: str
    formal: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime

    def __str__(self):
        return self.jenis_ptk
