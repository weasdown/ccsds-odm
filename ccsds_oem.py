# Container for data in an Orbit Ephemeris File (OEM). Defined based on CCSDS 502.0-B-3 section 5

from __future__ import annotations
from typing import Union

class Epoch:
    """
    Spacecraft epoch in ASCII time code A or B format (see 3.5.1.1/3.5.1.2 of CCSDS 301.0-B-4)
    """

    def __init__(self, year: str, month: str, day: str, hours: str, minutes: str, seconds: str, frac_seconds: str = None, day_of_year: str = None, time_code: str = None) -> None:
        pass
        # TODO add leading zeros if argument shorter than defined length

        self.year: str = year
        self.month: str = month

        # One of these is required:
        self.day: str = None if day is None else day  # two digit day of month
        self.day_of_year: str = None if day_of_year is None else day_of_year  # three digit day of year

        self.hours: str = hours
        self.minutes: str = minutes
        self.seconds: str = seconds
        self.frac_seconds: str = '' if frac_seconds is None else frac_seconds  # fractions of a second (optional)
        self.time_code: str = '' if time_code is None else 'Z'  # only permitted value is 'Z' for Zulu (UTC)

    def to_string(self, format: str = 'A'):
        frac_secs = f'.{self.frac_seconds}' if self.frac_seconds != '' else ''

        if format == 'A':
            base = f'{self.year}-{self.month}-{self.day}T{self.hours}:{self.minutes}:{self.seconds}'
            return base + frac_secs + self.time_code
        
        if format == 'B':
            base = f'{self.year}-{self.month}-{self.day_of_year}T{self.hours}:{self.minutes}:{self.seconds}'
            return base + frac_secs + self.time_code

class OEM:
    class Header:
        """
        See section 5.2.2
        """
        
        class Version:
            """
            Mandatory
            """
            def __init__(self, major: int, minor: int) -> None:
                self._major = major
                self._minor = minor

            def to_string(self) -> str:
                return f'{self._major}.{self._minor}'

        class Classification:
            """
            Optional
            """
            classification: str

            def to_string(self) -> str:
                return f'SBU {self.classification}'  # TODO check leading SBU in standard

        class CreationDate:
            """
            File creation date and time in UTC. See standard section 7.5.10.
            Mandatory
            """
            date_time: str

            def to_string(self)  -> str:
                return self.date
        
        class Originator:
            """
            The agency or operator that created the OEM file.
            Mandatory
            """
            def __init__(self, agency_operator: str) -> None:
                allowed_agency_operators = ['CNES', 'ESOC', ...]  # TODO: complete based on Annex B, B1 Abbreviation column or Name column if no Abbreviation
                if agency_operator in allowed_agency_operators:
                    self.agency_operator: str = agency_operator
                else:
                    raise ValueError('Invalid agency/operator')

            def to_string(self) -> str:
                raise NotImplementedError

        class MessageID:
            """
            Uniquely identifies a message from a given originator.
            Optional.
            Format and content of message identifier at discretion of operator.
            """

            def to_string(self) -> str:
                raise NotImplementedError

        def __init__(self, version: Version, comment: OEM.Comment) -> None:
            """
            Instantiate a Header
            """
            pass

        def to_string(self) -> str:
            raise NotImplementedError

    class Metadata:
        """
        See section 5.2.3
        """

        start = 'META_START'
        stop = 'META_STOP'

        def __init__(self, comment: OEM.Comment, object_name: str, object_id: str, center_name: str, ref_frame: str, ref_frame_epoch: str, time_system: str, start_time: str, stop_time: str, interpolation_degree: int, useable_start_time: str = None, useable_stop_time: str = None) -> None:
            """
            object_name: str: recommended to use names from UNOOSA designator index, which include Object name and international designator of the participant. If not listed in UNOOSA index, or content unknown/undisclosable, must be "UNKNOWN"
            object_id: str: recommended to use international spacecraft designator as in UNOOSA designator index. See page 5-5 for format.
            center_name: str: origin of OEM frame. For natural bodies choose from values in annex B, subsection B2. For spacecraft, use its OBJECT_ID or international designator.
            start_time: str: see 7.5.10.
            """
            pass

    class EphemerisData:
        def __init__(self, epoch, x, y, z, x_dot, y_dot, z_dot, x_ddot = None, y_ddot = None, z_ddot = None) -> None:  # TODO type annotations
            pass
        
        def to_string(self) -> str:
            return f'{self.epoch} {self.x} {self.y} {self.z} {self.x_dot} {self.y_dot} {self.z_dot} {self.x_ddot} {self.y_ddot} {self.z_ddot}' # TODO

    class CovarianceData:
        start = '\nCOVARIANCE_START\n'
        stop = '\nCOVARIANCE_STOP\n'

        def __init__(self, epoch, cov_ref_frame: str) -> None:
            pass

    class Comment:
        """
        Optional
        """
        comment: str

        def to_string(self) -> str:
            return f'COMMENT {self.comment}'

    def __init__(self) -> None:
        pass

    def valid(self) -> bool:
        """
        Check whether an OEM object is valid (e.g. header fields present as mandated by present data sections).
        
        Returns bool: True if valid, False if invalid or if error thrown during check.
        """
        pass


print(Epoch('2024', '05', '01', '0', '15', '23').to_string())
