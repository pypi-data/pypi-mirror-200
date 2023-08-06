from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.queries._SharedConverters import Mixin as _SharedConverters
from typing import Iterator
from sharingiscaring.GRPCClient.CCD_Types import CCD_DelegatorRewardPeriodInfo

class Mixin(_SharedConverters):
    def get_delegators_for_passive_delegation_in_reward_period(self, block_hash: str) -> list[CCD_DelegatorRewardPeriodInfo]:
        self.stub: QueriesStub
        result = []
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        
        grpc_return_value:Iterator[DelegatorInfo] = \
            self.stub.GetPassiveDelegatorsRewardPeriod(request=blockHashInput)
        
        for delegator in list(grpc_return_value):
            
            result.append( CCD_DelegatorRewardPeriodInfo(**{
                'account': self.convertAccountAddress(delegator.account),
                'stake':   self.convertAmount(delegator.stake)
            } ))

        return result