from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.queries._SharedConverters import Mixin as _SharedConverters
from typing import Iterator
from sharingiscaring.GRPCClient.CCD_Types import *
from rich import print

class Mixin(_SharedConverters):
    def convertFinalizedBlock(self, block) -> CCD_FinalizedBlockInfo:
        result = {}

        for descriptor in block.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, block)
                
                if type(value) in self.simple_types:
                    result[key] = self.convertType(value)

        return CCD_FinalizedBlockInfo(**result)

    def get_finalized_blocks(self) -> CCD_FinalizedBlockInfo:
        self.stub: QueriesStub
        
        for block in self.stub.GetFinalizedBlocks(request = Empty()):
            print (self.convertFinalizedBlock(block))       
            
