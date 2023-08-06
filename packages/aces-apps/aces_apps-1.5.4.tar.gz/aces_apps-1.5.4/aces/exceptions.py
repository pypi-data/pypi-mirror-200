class MissingBeamError(Exception):
    """Error raised when one of the 36 beams that form the PAF footprint is not found. 
    
    This is used primarily in cases of processing where 36 beams are expect, such as the SEFD and holography processing pipelines
    """
    
class MissingMSError(Exception):
    """Error raised when there is an unexpected number of measurement sets. 
    
    This is used primarily in cases of processing where 36 beams are expect, such as the SEFD and holography processing pipelines,
    but is slightly more generalised to account for other situations
    """