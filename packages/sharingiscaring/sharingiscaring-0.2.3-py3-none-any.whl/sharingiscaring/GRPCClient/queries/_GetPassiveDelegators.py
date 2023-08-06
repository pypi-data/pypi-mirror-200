from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.queries._SharedConverters import Mixin as _SharedConverters
from typing import Iterator
from sharingiscaring.GRPCClient.CCD_Types import CCD_DelegatorInfo

class Mixin(_SharedConverters):
    def get_delegators_for_passive_delegation(self, block_hash: str) -> list[CCD_DelegatorInfo]:
        self.stub: QueriesStub
        result: list[CCD_DelegatorInfo] = []
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        
        grpc_return_value:Iterator[DelegatorInfo] = \
            self.stub.GetPassiveDelegators(request=blockHashInput)
        
        for delegator in list(grpc_return_value):
            
            delegator_dict = {
                'account': self.convertAccountAddress(delegator.account),
                'stake':   self.convertAmount(delegator.stake)
                }
            if delegator.pending_change:
                if self.valueIsEmpty(delegator.pending_change):
                    pass
                else:
                    delegator_dict.update({
                        'pending_change': self.convertPendingChange(delegator.pending_change)
                    })

            result.append( CCD_DelegatorInfo(**delegator_dict ))

        return result