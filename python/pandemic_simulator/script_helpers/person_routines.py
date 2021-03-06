# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.
from typing import Sequence, Type, Optional

import numpy as np

from ..environment import LocationID, PersonRoutine, Registry, SimTimeInterval, GroceryStore, \
    RetailStore, BarberShop, Retired

__all__ = ['get_minor_routines', 'get_adult_routines']


def get_minor_routines(home_id: LocationID,
                       registry: Registry,
                       numpy_rng: Optional[np.random.RandomState] = None) -> Sequence[PersonRoutine]:
    routines = []
    numpy_rng = numpy_rng if numpy_rng is not None else np.random.RandomState()

    barber_shops = registry.location_ids_of_type(BarberShop)
    if len(barber_shops) > 0:
        routines.append(PersonRoutine(start_loc=home_id,
                                      end_loc=barber_shops[numpy_rng.randint(0, len(barber_shops))],
                                      trigger_interval=SimTimeInterval(day=30)))

    return routines


def get_adult_routines(person_type: Type,
                       home_id: LocationID,
                       registry: Registry,
                       numpy_rng: Optional[np.random.RandomState] = None) -> Sequence[PersonRoutine]:
    routines = []
    numpy_rng = numpy_rng if numpy_rng is not None else np.random.RandomState()

    shopping_rate = 1 if isinstance(person_type, Retired) else 1
    grocery_stores = registry.location_ids_of_type(GroceryStore)
    if len(grocery_stores) > 0:
        interval_in_days = int(7 / shopping_rate)
        routines.append(PersonRoutine(start_loc=None,
                                      end_loc=grocery_stores[numpy_rng.randint(0, len(grocery_stores))],
                                      trigger_interval=SimTimeInterval(day=interval_in_days,
                                                                       offset_day=numpy_rng.randint(0,
                                                                                                    interval_in_days)),
                                      end_locs=grocery_stores,
                                      explore_probability=0.05))

    retail_stores = registry.location_ids_of_type(RetailStore)
    if len(retail_stores) > 0:
        interval_in_days = int(7 / shopping_rate)
        routines.append(PersonRoutine(start_loc=None,
                                      end_loc=retail_stores[numpy_rng.randint(0, len(retail_stores))],
                                      trigger_interval=SimTimeInterval(day=interval_in_days,
                                                                       offset_day=numpy_rng.randint(0,
                                                                                                    interval_in_days)),
                                      end_locs=retail_stores,
                                      explore_probability=0.05))

    barber_shops = registry.location_ids_of_type(BarberShop)
    if len(barber_shops) > 0:
        interval_in_days = 30
        routines.append(PersonRoutine(start_loc=home_id,
                                      end_loc=barber_shops[numpy_rng.randint(0, len(barber_shops))],
                                      trigger_interval=SimTimeInterval(day=interval_in_days,
                                                                       offset_day=numpy_rng.randint(0,
                                                                                                    interval_in_days))
                                      )
                        )

    return routines
