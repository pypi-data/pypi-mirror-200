from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.queries._SharedConverters import Mixin as _SharedConverters
from typing import Iterator
from sharingiscaring.GRPCClient.CCD_Types import *

class Mixin(_SharedConverters):
    def get_anonymity_revokers(self, block_hash: str) -> list[CCD_ArInfo]:
        self.stub: QueriesStub
        result = []
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        
        grpc_return_value:Iterator[ArInfo] = \
            self.stub.GetAnonymityRevokers(request=blockHashInput)
        
        for ar in list(grpc_return_value):
            
            result.append( self.convertArInfo(ar) )

        return result