import abc
from typing import Dict, Any, Optional

class BaseBankAdapter(abc.ABC):
    """
    Abstract base class for standard operations across all banks.
    All bank adapters must implement these standard operations.
    """

    @abc.abstractmethod
    def generate_bank_slip(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate (issue) a new bank slip."""
        pass

    @abc.abstractmethod
    def list_bank_slips(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List existing bank slips with optional filters."""
        pass

    @abc.abstractmethod
    def cancel_bank_slip(self, bank_slip_id: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Cancel an existing bank slip."""
        pass

    @abc.abstractmethod
    def edit_bank_slip(self, bank_slip_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Edit an existing bank slip."""
        pass

    def search_workspaces(self) -> dict:
        raise NotImplementedError
