import qlib

import os
_provider = os.environ.get("QLIB_DATA_DIR", os.environ.get("QLIB_PROVIDER_URI", "~/.qlib/qlib_data/cn_data"))
qlib.init(provider_uri=_provider)
from qlib.data import D

instruments = D.instruments()
fields = ["$open", "$close", "$high", "$low", "$volume"]  # , "$amount", "$turn", "$pettm", "$pbmrq"
data = D.features(instruments, fields, freq="day").swaplevel().sort_index().loc["2015-01-01":].sort_index()

# Calculate return per instrument. The index is (datetime, instrument) after swaplevel,
# so grouping by level 0 would compute a cross-sectional change across stocks instead.
data["$return"] = data.groupby(level="instrument")["$close"].pct_change().fillna(0)

print(data)

data.to_hdf("./daily_pv_all.h5", key="data")

fields = ["$open", "$close", "$high", "$low", "$volume"]  # , "$amount", "$turn", "$pettm", "$pbmrq"
data = (
    (
        D.features(instruments, fields, freq="day")
        .swaplevel()
        .sort_index()
    )
    .swaplevel()
    .loc[data.reset_index()["instrument"].unique()[:100]]
    .swaplevel()
    .sort_index()
)

# Calculate return per instrument (see note above)
data["$return"] = data.groupby(level="instrument")["$close"].pct_change().fillna(0)
print(data)
data.to_hdf("./daily_pv_debug.h5", key="data")