"""Caso de uso para listar todas las brigadas.

Proporciona una capa de aplicación sobre el repositorio, permitiendo
extender validaciones o filtrados futuros sin acoplar el router al
acceso directo de persistencia.
"""
from __future__ import annotations

from typing import List

from src.Modules.Brigadas.Domain.brigada import BrigadaSalida
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository


class ListarBrigadas:
    """Orquesta la obtención de todas las brigadas.

    Actualmente delega directamente en el repositorio. Se deja este caso
    de uso para mantener la uniformidad de la capa Application y poder
    añadir reglas (cache, filtrado por usuario, paginación) sin modificar
    el router.
    """

    def __init__(self, brigada_repository: BrigadaRepository) -> None:
        self.brigada_repository = brigada_repository

    def execute(self) -> List[BrigadaSalida]:
        """Retorna la lista completa de brigadas disponibles."""
        return self.brigada_repository.listar_brigadas()
