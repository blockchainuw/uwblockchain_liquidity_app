from dotenv import load_dotenv
import os
from web3 import Web3
from utils.ContractService import ContractService

# AaveService
# Encapsulates all functionality related to Aave
# default instantiatiation will connect 
class AaveLpService(object):
    @classmethod
    def __init__(cls) -> None:
        # instantiate Contract Service
        load_dotenv("./.env")
        cls.contractAddress = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
        cls.contractImplementationAddress = "0xc6845a5c768bf8d7681249f8927877efda425baf"
        try:
            cls.contractService = ContractService(
                apiKey=os.getenv("API_KEY"), 
                nodeAddress=os.getenv("NODE_ADDRESS"),
                contractAddress=cls.contractAddress,
                implementationAddress=cls.contractImplementationAddress
            )
        except:
            raise Exception("Failed to create ContractService for AaveProtocolDataProvider contract. Verify your .env file.")

        # connect to the Aave contract
        try:
            cls.contract = cls.contractService.connectImplementation()
        except:
            raise Exception("Failed to connect to AaveProtocolDataProvider Contract.")
            
    def listenToEvents(cls) -> None:
        print("----------------- LISTENING TO EVENTS... -----------------")
        eventFilter = cls.contract.events.Withdraw.createFilter(fromBlock="latest")
        
        while True:
            for event in eventFilter.get_new_entries():
                print("----------------- NEW EVENT -----------------")
                print(Web3.toJSON(event))
