from typing import Union
from abc import ABC, abstractmethod


import numpy as np
import numpy.typing as npt

# from pyprotolinc.assumptions.providers import ZeroRateProvider
# from pyprotolinc.assumptions.providers import ConstantRateProvider
# from pyprotolinc.assumptions.providers import StandardRateProvider
import pyprotolinc._actuarial as act  # type: ignore
from pyprotolinc.assumptions.providers import BaseRatesProvider
from pyprotolinc.riskfactors.risk_factors import RiskFactor


class AbstrAssumptionsTable(ABC):
    """ Abstract base class for the assumption table classes. """

    @abstractmethod
    def rates_provider(self) -> Union[act.StandardRateProvider, BaseRatesProvider]:
        pass


class ScalarAssumptionsTable(AbstrAssumptionsTable):
    """ Represents a 0-dimensional (i.e. scalar) assumption. """

    def __init__(self, const_value: float) -> None:
        self.const_value = const_value

    def rates_provider(self) -> BaseRatesProvider:
        b: BaseRatesProvider = act.ConstantRateProvider(self.const_value)
        return b


class AssumptionsTable1D(AbstrAssumptionsTable):
    """ Represents a 1D assumption table. """

    def __init__(self, values: npt.NDArray[np.float64], risk_factor_class: type[RiskFactor], offset: int = 0):
        self.offset = offset
        # assert values is a numpy array
        shape = values.shape
        dims = len(shape)
        if dims == 2:
            if shape[0] > 1 and shape[1] > 1:
                raise Exception("Wrong dimension passed in for 1D assumptions table: {}".format(str(shape)))
            elif shape[1] == 1:
                values = values.reshape((shape[0],))
            else:
                values = values.reshape((shape[1],))
        elif dims > 2:
            raise Exception("Wrong dimension passed in for 1D assumptions table: {}".format(str(shape)))

        req_length = risk_factor_class.required_length()
        if req_length:
            assert req_length == len(values), "Required length of assumptions does not fit for {}".format(
                risk_factor_class.__name__
            )
        self.values = values.astype(np.float64)
        self.risk_factor_class = risk_factor_class

    def rates_provider(self) -> act.StandardRateProvider:  # BaseRatesProvider:
        # return StandardRateProvider(self.values, (self.risk_factor_class,), offsets=(self.offset,))
        return act.StandardRateProvider(rfs=[self.risk_factor_class.get_CRiskFactor()],
                                        values=self.values,
                                        offsets=np.array([self.offset, ], dtype=np.int32))


class AssumptionsTable2D(AbstrAssumptionsTable):
    """ Represents a 2D assumption table. """

    def __init__(self,
                 values: npt.NDArray[np.float64],
                 risk_factor_class_v: type[RiskFactor],
                 risk_factor_class_h: type[RiskFactor],
                 v_offset: int = 0,
                 h_offset: int = 0):
        self.v_offset = v_offset
        self.h_offset = h_offset
        # assert values is a numpy array
        shape = values.shape
        if len(shape) != 2:
            raise Exception("Wrong dimension passed in for 1D assumptions table: {}".format(str(shape)))

        req_length_v = risk_factor_class_v.required_length()
        req_length_h = risk_factor_class_h.required_length()
        if req_length_v:
            assert req_length_v == shape[0], "Vertical length of assumptions does not fit for {}".format(
                risk_factor_class_v.__name__
            )
        if req_length_h:
            assert req_length_h == shape[1], "Horizontal length of assumptions does not fit for {}".format(
                risk_factor_class_h.__name__
            )

        self.values = values.astype(np.float64)

        self.risk_factor_class_v = risk_factor_class_v
        self.risk_factor_class_h = risk_factor_class_h

    def rates_provider(self) -> act.StandardRateProvider:  # -> BaseRatesProvider:
        # return StandardRateProvider(self.values, (self.risk_factor_class_v, self.risk_factor_class_h),
        #                            offsets=(self.v_offset, self.h_offset))

        return act.StandardRateProvider(rfs=[self.risk_factor_class_v.get_CRiskFactor(),
                                        self.risk_factor_class_h.get_CRiskFactor()],
                                        values=self.values,
                                        offsets=np.array((self.v_offset, self.h_offset), dtype=np.int32))
