import sys
import threading
import queue

from datetime import datetime

import oracledb

from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.migration_properties import MigrationProperties
from src.mb_cruise_migration.models.intermediary.cruise_cargo import CruiseCargo
from src.mb_cruise_migration.models.intermediary.mb_cargo import MbCargo
from src.mb_cruise_migration.framework.consts.const_initializer import ConstInitializer
from src.mb_cruise_migration.processors.cruise_processor import CruiseProcessor
from src.mb_cruise_migration.processors.transfer_station import TransferStation
from src.mb_cruise_migration.logging.migration_report import MigrationReport
from src.mb_cruise_migration.processors.mb_processor import MbProcessor
from src.mb_cruise_migration.utility.common import strip_none


class Migrator(object):
    def __init__(self, config_file):
        MigrationProperties(config_file)
        MigrationLog()
        MigrationReport()
        if MigrationProperties.cruise_db_config.pooled:
            oracledb.init_oracle_client()
        self.mb_processor = MbProcessor()

    def migrate(self):

        self.start_migration()

        shipping_queue = queue.Queue(MigrationProperties.run_parameters.max_queue_size)

        producer = threading.Thread(target=self.producer, args=(shipping_queue,))
        consumer = threading.Thread(target=self.consumer, args=(shipping_queue,))

        consumer.start()
        producer.start()

        producer.join()
        consumer.join()

        self.end_migration()

    def producer(self, shipping_queue):
        """
        producer thread pulls survey-centric related objects out of the MB
        schema in paginated groups and then converts them to dataset-centric
        groupings of related objects before adding them to the queue.
        """
        try:
            while not self.mb_processor.surveys_exhausted():
                mb_cargo = self.get_next_shipment()
                cruise_cargo = self.prepare_shipment(mb_cargo)
                shipping_queue.put(cruise_cargo, block=True, timeout=None)
        except Exception as e:
            MigrationLog.log_exception(e)
            self.fail_migration("producer", e)
        finally:
            shipping_queue.put(None)  # sentinel value (finish)

    def consumer(self, shipping_queue):
        """
        consumer thread pulls dataset-centric groupings of related objects off
        of the queue one at a time and then inserts them into the cruise schema.
        """
        while True:
            cruise = shipping_queue.get(block=True, timeout=None)
            if cruise is None:
                break
            self.ship_to_cruise(cruise)

    def start_migration(self):
        MigrationLog.log_start()
        MigrationReport.start = datetime.now()
        try:
            ConstInitializer.initialize_consts()
        except Exception as e:
            MigrationLog.log_exception(e)
            self.fail_migration("const initializer", e)

    def get_next_shipment(self) -> [MbCargo]:
        return self.mb_processor.load()

    @staticmethod
    def prepare_shipment(mb_crates) -> [CruiseCargo]:
        stations = [TransferStation(crate) for crate in mb_crates]
        cruise_cargos = strip_none([station.transfer() for station in stations])
        return [cargo for cruise_cargo in cruise_cargos for cargo in cruise_cargo]  # flatten

    @staticmethod
    def ship_to_cruise(shipment):
        CruiseProcessor().ship(shipment)

    @staticmethod
    def end_migration():
        MigrationLog.log_end()
        MigrationReport.end = datetime.now()
        MigrationReport.migration_final_report()

    @staticmethod
    def fail_migration(context, exception: Exception):
        MigrationReport.failure_message = f"Fatal failure occurred in {context}: \n\t{str(exception)}"
        MigrationReport.success = False
        # self.end_migration(success=False)
        # sys.exit(1)
