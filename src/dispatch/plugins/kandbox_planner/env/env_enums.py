from enum import Enum


class PlannerType(str, Enum):
    SINGLE = "single"
    PICKDROP = "pickdrop"


# F=Floating (which is free/movable, with in-planning job_ids), ABS = absence shared visits is here
# J=job (Planned), and J includes A=appointment (Fixed Job) , EX=Exception (conflicted jobs?),  ?
# Maybe in future track "Vacuum Space" to schedule non-working hour jobs? as long as they are not conflicting with other assigned jobs.
class TimeSlotType(str, Enum):
    FLOATING = "F"
    JOB_FIXED = "J"
    # ABSENCE = "E"



class TimeSlotOperationType(str, Enum):
    UPDATE = "U"
    DELETE = "D"


class ActionType(str, Enum):
    # F=Floating (which is free/movable, with in-planning job_ids),
    # J=job (Planned), EX=Exception (conflicted jobs?),
    # A=appointment (Fixed Job) ,
    # ABS = absence shared visits is here? Maybe in future track "Vacuum Space" to schedule non-working hour jobs? as long as they are not conflicting with other assigned jobs.
    FLOATING = "F"
    JOB_FIXED = "J"
    UNPLAN = "U"  #
    TODO = 'TD'
    SAVED_TO_ENV = 'SAVED'
    FINISHED = 'FIN'
    DELAY_BLOCKED = 'DELAY'


class ActionCommandType(int, Enum):
    # Three types of actions:
    # 0. idle - does nothing
    # 1. dispatch - plan current unplanned_job to a specifc worker slot. The worker slot index is pointing to obs["slots"]
    # 2. reposition - select one worker and move him on map to a specifiy longitude/latitude.

    IDLE = 0
    DISPATCH = 1
    REPOSITION = 2

    # 2. move - select one worker and move him on map to a specifiy longitude/latitude.

class WorkerType(str, Enum):
    """ WorkerType defines types of workers with different role of function

    WORKER is one person which can work as primary.
    Secondary must work with another primary in a shared job. A secondary worker can move on its own, but a vehicle can not.
    Vehicle: A container that CAN move, which item tracking. 
        Only the shared, swappable vehicles should be tracked. If a vehicle is permenantly 
        used by a primary worker, it should be inside primary worker flex form.

    Depot: A container that can NOT move. (MAY be not a worker?)
    """

    WORKER = "W"
    SECONDARY = "S"
    VEHICLE = "V" 

    # DEPOT = "D"

class JobType(str, Enum):
    """
    COMPOSITE is a (virtual) job containing multiple jobs. The included jobs must be assigned to a same set workers.
    -- A composite will be treated virtual, and its included jobs are scheduled individually, but must be assigned to a same worker.

    APPOINTMENT is also a composite job with permenant P status. The AI engine should not attempt to change its planning status/data.
    -- An appointment will be treated as one continuous time unit and it hides all its included jobs. appt is equal to "composite (or normal) + fixed_time". It may or maynot have included_jobs...

    JOB == "visit": JOB means that this is a atomic job and does not include other jobs. JOB also means it is regular job to be planned, not a sub-job.
    ABSENCE = "event": when a worker can not performce the job.
    """

    JOB = "visit"

    # 2022-12-09 16:53:55 a composite is a pickdrop order.
    # COMPOSITE = "composite"
    # 2022-12-09 16:53:55 appt should be moved to order
    APPOINTMENT = "appt"
    
    ABSENCE = "event"
    REPLENISH = "replenish"
    
    # Till 2022-02-11 16:59:13, I am still using suffix in job code to tell it is pick or drop.
    # PICK = "pick"
    # DROP = "drop"
    
    # 2021-10-23 08:15:39 lunch_break is not same as replenish, I have not yet decided to include it.
    # LUNCH_BREAK = "lunch_break"


class JobPlanningStatus(str, Enum):
    """Planning Status for JOB. 
    \n U == Un-planned. When is Job is U status, the scheduled information (scheduled_start/duration/workers) is ignored. 
    \n I == In-planning. When is Job is I status, the scheduled attributes must have valid values. 
    \n P == Planned. When is Job is P status, it is treated as fixed agreement for both worker assignment and datetime. The easydispatch engine will not modify its scheduling information.  
    \n C == CANCELLED. When is Job is C status, it will be removed. In future, it will be moved to historical storage. DO NOT USE THIS STATUS.
    \n F == FINISHED. When is Job is F status, it will be moved to historical storage. 
    """
    IN_PLANNING = "I"
    UNPLANNED = "U"
    PLANNED = "P"
    CANCELLED = "C"
    FINISHED = "F"   # maps to visited=V
    
class JobLifeCycleStatus(str, Enum):
    """Planning Status for JOB. 
    \n Created: default status for all new jobs. If this column is not used in any given team, the life cycle status should always remain Created. 
    \n Started: When the worker check in onsite.
    \n Item_Ready: All items(materials) needed for this job are ready (on the van, or with workers) 
    \n FINISHED (F): The workers have Completed the onsite job. This is aligned with planning_status == F
    """
    CREATED = "Created"
    TRAVEL_STARTED = "Travel_Started"
    ONSITE_STARTED = "Onsite_Started"
    ITEM_READY = "Item_Ready"
    FINISHED = "F"
    CUSTOMER_APPROVED = "Customer_Approved"
    PLANNER_APPROVED = "Planner_Approved"
    CANCELLED = "Cancelled"
    ARCHIVED = "Archived"

    PAID = "Paid"
    VIRTUAL_JOB = "VIRTUAL_JOB" # Status can not be changed.
    UNKNOWN = "UNKNOWN"
    
    ARRIVED = "arrived"
    DELIVERY = "delivery"



JobLifeCycleStatus_SEQUENCE = {
    JobLifeCycleStatus.CREATED: 0,
    JobLifeCycleStatus.ARRIVED: 1,

    JobLifeCycleStatus.TRAVEL_STARTED: 3,
    JobLifeCycleStatus.ONSITE_STARTED: 3,
    JobLifeCycleStatus.ITEM_READY: 3,

    JobLifeCycleStatus.FINISHED: 10, 

    JobLifeCycleStatus.CUSTOMER_APPROVED: 20,
    JobLifeCycleStatus.PLANNER_APPROVED: 30,

    JobLifeCycleStatus.ARCHIVED: 100,
    JobLifeCycleStatus.CANCELLED: 100,

    JobLifeCycleStatus.UNKNOWN: 100,
    JobLifeCycleStatus.PAID: 100,
    JobLifeCycleStatus.VIRTUAL_JOB: 100,
}




class JobScheduleType(str, Enum):
    FIXED_SCHEDULE = "FS"
    NORMAL = "N"
    FIXED_DATE = "FD"
    FIXED_TIME = "FT"
    NEED_APPOINTMENT = "NA"
    # NIGHT_SCHEDULE = "NN"


class LocationType(str, Enum):
    """ H="Home", J=Job,  """

    HOME = "H"
    JOB = "J"
    ABSENCE = "ABS"



class AppointmentStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"
    NOT_APPOINTMENT = "NOT_APPOINTMENT"


AppointmentStatus_SEQUENCE = {
    AppointmentStatus.PENDING: 0,
    AppointmentStatus.READY: 3,
    AppointmentStatus.CANCELLED: 3,
    AppointmentStatus.ERROR: 3,
    AppointmentStatus.EXPIRED: 3,
    AppointmentStatus.UNKNOWN: 100,
}




# 'replay' for replay Planned jobs, where allows conflicts. "predict" for training new jobs and predict.
class EnvRunModeType(str, Enum):
    PREDICT = "predict"
    REPLAY = "replay"


class OptimizerSolutionStatus(Enum):
    SUCCESS = 0
    INFEASIBLE = 1
    INPUT_VALIDATION_ERROR = 2


class ActionScoringResultType(str, Enum):
    OK = "OK"
    WARNING = "Warning"
    ERROR = "Error"
    RECOMMENDED_SLOT_DAMAGED = "RECOMMENDED_SLOT_DAMAGED"  # "CODE_40014"


class ActionScoringMetricsCode(str, Enum):
    COMPOSITION_SHARED_JOBS = "composition_shared_jobs"
    WORKING_HOUR = "Within Working Hour"
    ENOUGH_TRAVEL = "Enough Travel"
    LUNCH_BREAK = "Lunch Break"
    REQUESTED_SKILLS = "Requested Skills"




class OrderCreateResultStatusType(str, Enum):
    CREATION_FAILED = "CREATION_FAILED"
    CREATED_AND_DISPATCHED = "DISPATCHED"
    CREATED_AND_COMMITTED = "COMMITTED"
    CREATED_BUT_NOT_DISPATCHED = "CREATED"
    CREATED_BUT_DISPATCH_FAILED = "DISPATCH_FAILED"
    CREATED_BUT_COMMIT_FAILED = "COMMIT_FAILED"




###########################################################################
##   Kafka   ###
###########################################################################


class KafkaRoleType(str, Enum):
    FAKE = "FAKE"  # It does nothing
    PRODUCER_ONLY = "PRODUCER_ONLY"  # Can produce messages, but not consume
    ENV_ADAPTER = "ENV_ADAPTER"
    RECOMMENDER = "RECOMMENDER"  # with all


class KafkaMessageType(str, Enum):
    CREATE_WORKER = "Create_Worker"
    CREATE_JOB = "Create_Job"  # from GTS loading
    CREATE_APPOINTMENT = "Create_Appointment"
    CREATE_ABSENCE = "Create_Absence"

    UPDATE_WORKER = "Update_Worker"
    UPDATE_WORKER_ATTRIBUTES = "Update_Worker_Attributes"  # REFRESH_WORKER = "Refresh_Worker"  #
    # UPDATE_JOB will update only the attribute and will NOT re-schedule the job.
    UPDATE_JOB = "Update_Job"  # from
    # When planning info is changed, do not use UPDATE_JOB, use RESCHEDULE_JOB.
    RESCHEDULE_JOB = "Reschedule_Job"
    # REFRESH_JOB will be used once the job is applied to timeslot server. Other env instances shall use this message to refresh its local cache.
    REFRESH_JOB = "Refresh_Job"
    UPDATE_APPOINTMENT = "Update_Appointment"
    UPDATE_ABSENCE = "Update_Absence"

    DELETE_WORKER = "Delete_Worker"
    DELETE_JOB = "Delete_Job"  # from GTS loading
    DELETE_APPOINTMENT = "Delete_Appointment"
    DELETE_ABSENCE = "Delete_Absence"

    UPDATE_PLANNING_WINDOW = "Update_Planning_Window"
    REFRESH_PLANNING_WINDOW = "Refresh_Planning_Window"
    REFRESH_RECOMMENDATION = "Refresh_Recommendation"
    REFRESH_RECOMMENDATION_SINGLE_APPOINTMENT = "Refresh_Recommendation_Single_Appointment"

    DELETE_WORKING_TIME_SLOTS = "Delete_Slots"  # Includes deleted and inserted.
    UPDATE_WORKING_TIME_SLOTS = "Update_Slots"  # Includes deleted and inserted.
    POST_CHANGED_JOBS = "Post_Changed_Jobs"  # Includes deleted and inserted.


class KandboxMessageTopicType(str, Enum):
    ENV_WINDOW = "input"
    ENV_WINDOW_OUTPUT = "output"


class KandboxMessageSourceType(str, Enum):
    ENV = "ENV"
    PLANNER_UI = "Planner_UI"
    BATCH_INPUT = "Batch_Input"
    REST_API = "Rest_API"
    SYSTEM = "SYSTEM"




class EnvStepType(int, Enum):
    # Three types of actions:
    # 0. idle - does nothing
    # 1. dispatch - plan current unplanned_job to a specifc worker slot. The worker slot index is pointing to obs["slots"]
    # 2. reposition - select one worker and move him on map to a specifiy longitude/latitude.

    JOB2SLOT = 0
    TSP_SELECTION = 1
    TSP_SWAP = 2

class WorkerStatusUpdateType(str, Enum):
    BEGIN_SHIFT = "begin_shift"
    END_SHIFT = "end_shift"
    UPDATE_LOCATION = "update_location"
    ACCUM_ITEMS = "accum_items"



class KandboxPlannerPluginType(str, Enum):
    kandbox_env_proxy = "kandbox_env_proxy"
    kandbox_env = "kandbox_env"
    configurable_kandbox_env = "configurable_kandbox_env"
    kandbox_agent = "kandbox_agent"
    kandbox_batch_optimizer = "kandbox_batch_optimizer"
    internal_dispatcher = "internal_dispatcher"
    kandbox_simple_optimizer = "kandbox_simple_optimizer"
    kandbox_rule = "kandbox_rule"
    kandbox_worker_check_rule = "worker_check_rule"
    kandbox_data_adapter = "kandbox_data_adapter"
    kandbox_data_generator = "kandbox_data_generator"
    kandbox_location_service = "kandbox_location_service"
    # kandbox_routing_adapter should be named as kandbox_algorithm_routing 2022-09-22 00:40:40
    kandbox_routing_adapter = "kandbox_routing_adapter"
    kandbox_frontend_routing_adapter = "kandbox_frontend_routing"
    kandbox_kafka_handler = "kandbox_kafka_handler"


