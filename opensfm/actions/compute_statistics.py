import logging
import os

from opensfm import io
from opensfm import stats

logger = logging.getLogger(__name__)


def run_dataset(data):
    """Compute various staistics of a datasets and write them to 'stats' folder

    Args:
        data: dataset object

    """
    reconstructions = data.load_reconstruction()
    tracks_manager = data.load_tracks_manager()

    output_path = os.path.join(data.data_path, "stats")
    io.mkdir_p(output_path)

    stats_dict = stats.compute_all_statistics(data, tracks_manager, reconstructions)

    # that's a bit hacky but recomputing projection error doesn't come for free
    stats.save_residual_grids(data, tracks_manager, reconstructions, output_path)
    stats.save_matchgraph(data, tracks_manager, reconstructions, output_path)
    stats.save_heatmap(data, tracks_manager, reconstructions, output_path)

    with io.open_wt(os.path.join(output_path, "stats.json")) as fout:
        io.json_dump(stats_dict, fout)
