#!/usr/bin/env python
import argparse
import json
import logging
import os
import sys
import tarfile
import time
from zipfile import ZipFile

from beauris import Beauris


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def replace_fake_files(twobit_file, output, to_swap, zipf):

    with tarfile.open(output, 'w:gz') as tarf:
        for zip_info in zipf.infolist():
            if zip_info.filename.startswith('data/'):
                filename = zip_info.filename[5:]
                tar_info = tarfile.TarInfo(name=filename)
                tar_info.mtime = time.mktime(tuple(zip_info.date_time) + (-1, -1, -1))
                if filename in to_swap:
                    log.info("Replacing archive file {} by symlink to {}".format(filename, to_swap[filename]))
                    tar_info.type = tarfile.SYMTYPE
                    tar_info.linkname = to_swap[filename]
                    tarf.addfile(
                        tarinfo=tar_info
                    )
                else:
                    tar_info.size = zip_info.file_size
                    tarf.addfile(
                        tarinfo=tar_info,
                        fileobj=zipf.open(zip_info.filename)
                    )

        # Add 2bit file
        tarf.add(twobit_file, arcname="./searchDatabaseData/genome.2bit")


def add_tracks_in_category(cat, tracks, group_num, upload_prefix="track", track_type=None):
    track_group = "track_groups_{}".format(group_num)
    track_params = {"{}|category".format(track_group): cat}
    tool_params = {}
    tool_params.update(track_params)

    datasets_by_types = {}

    for track in tracks:

        if track_type is None:
            track_type = track.type

        if track_type not in datasets_by_types:
            datasets_by_types[track_type] = []

        datasets_by_types[track_type].append(
            {
                "id": "##UPLOADED_DATASET_ID__{}_{}##".format(upload_prefix, track.name),
                "src": "hda",
            }
        )

    for track_type in datasets_by_types:
        track_num = 0
        param_prefix = "{}|data_tracks_{}|data_format|".format(track_group, track_num)
        track_params = {
            param_prefix + "annotation": {
                "batch": False,
                "values": datasets_by_types[track_type]
            },
        }

        if track_type == "rnaseq":
            track_params.update({
                param_prefix + "data_format_select": "pileup",
                param_prefix + "auto_snp": "true",
                param_prefix + "chunkSizeLimit": "5000000",
                param_prefix + "track_visibility": "default_off",
                param_prefix + "override_apollo_drag": "False",
                param_prefix + "override_apollo_plugins": "False",
            })

        elif track_type == "gff":
            track_params.update({
                param_prefix + "data_format_select": "gene_calls",
                param_prefix + "index": "true",
                param_prefix + "jbcolor_scale|color_score|color_score_select": "none",
                param_prefix + "jbcolor_scale|color_score|color|color_select": "automatic",

                param_prefix + "jbstyle|max_height": "600",
                param_prefix + "jbstyle|style_classname": "transcript",
                param_prefix + "jbstyle|style_description": "note,description",
                param_prefix + "jbstyle|style_height": "10px",
                param_prefix + "jbstyle|style_label": "product,name,id",
                param_prefix + "match_part|match_part_select": "false",
                param_prefix + "override_apollo_drag": "False",
                param_prefix + "override_apollo_plugins": "False",
                param_prefix + "track_config|html_options|topLevelFeatures": "",
                param_prefix + "track_config|track_class": "NeatHTMLFeatures/View/Track/NeatFeatures",
                param_prefix + "track_visibility": "default_off",
            })

        elif track_type == "wig":
            track_params.update({
                param_prefix + "data_format_select": "wiggle",
                param_prefix + "jbcolor|bicolor_pivot|bicolor_pivot_select": "zero",
                param_prefix + "jbcolor|color|color_select": "automatic",
                param_prefix + "xyplot": "true",
                param_prefix + "var_band": "false",
                param_prefix + "scaling|scale_select": "auto_local",
                param_prefix + "MultiBigWig": "false",
                param_prefix + "track_visibility": "default_off",
                param_prefix + "override_apollo_drag": "False",
                param_prefix + "override_apollo_plugins": "False",
            })

        tool_params.update(track_params)

    return tool_params


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    task_id = "jbrowse"

    exit_code_all = 0

    for ass in org.assemblies:

        file_uploads = {}
        file_uploads['ass_{}'.format(ass.slug(short=True))] = {'type': 'fasta', 'path': ass.get_input_path('fasta'), 'name': ass.slug(short=True)}

        for annot in ass.annotations:
            file_uploads['annot_{}'.format(annot.version)] = {'type': 'gff', 'path': annot.get_derived_path('fixed_gff'), 'name': annot.version}

        for track in ass.tracks:
            if track.input_files['track_file'].type == 'bam':
                # TODO make this trick more documented/configurable
                # Bam files are huge, and the galaxy tool doesn't read them much.
                # So don't send them, send a fake tiny bam, and we'll replace it after job completion
                fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../test-data/data/file.bam')
            else:
                fpath = track.get_input_path('track_file')
            file_uploads['track_{}'.format(track.name)] = {'type': track.input_files['track_file'].type, 'path': fpath, 'name': track.name}

            if track.input_files['track_file'].type == 'bam':
                # If it's a bam, it means we have a bigwig file too, upload a tiny fake one as we do for bams
                wigpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../test-data/data/file.wg')
                file_uploads['track_wig_{}'.format(track.name)] = {'type': 'bigwig', 'path': wigpath, 'name': track.name}

        # Use a precise tool version if possible
        # tool = "JBrowse"
        tool = "toolshed.g2.bx.psu.edu/repos/iuc/jbrowse/jbrowse/1.16.11+galaxy1"

        tool_params = {
            "action|action_select": "create",
            "gencode": "1",
            "jbgen|aboutDescription": "",
            "jbgen|defaultLocation": "",
            "jbgen|hideGenomeOptions": "false",
            "jbgen|shareLink": "true",
            "jbgen|show_menu": "true",
            "jbgen|show_nav": "true",
            "jbgen|show_overview": "true",
            "jbgen|show_tracklist": "true",
            "jbgen|trackPadding": 20,
            "plugins|BlastView": "true",
            "plugins|ComboTrackSelector": "false",
            "plugins|GCContent": "false",
            "reference_genome|genome": {
                "batch": False,
                "values": [
                    {
                        "id": "##UPLOADED_DATASET_ID__ass_{}##".format(ass.slug(short=True)),
                        "src": "hda",
                    }
                ]
            },
            "reference_genome|genome_type_select": "history",
            "standalone": "minimal",
            "track_groups_0|category": "Annotation",
            "uglyTestingHack": ""
        }

        group_num = 0

        annot_track_group = "track_groups_{}".format(group_num)
        track_num = 0
        for annot in ass.annotations:
            param_prefix = "{}|data_tracks_{}|data_format|".format(annot_track_group, track_num)
            track_params = {
                param_prefix + "annotation": {
                    "batch": False,
                    "values": [
                        {
                            "id": "##UPLOADED_DATASET_ID__annot_{}##".format(annot.version),
                            "src": "hda",
                        }
                    ]
                },
                param_prefix + "data_format_select": "gene_calls",
                param_prefix + "index": "true",
                param_prefix + "jbcolor_scale|color_score|color_score_select": "none",
                param_prefix + "jbcolor_scale|color_score|color|color_select": "automatic",

                # param_prefix + "jbmenu|track_menu_0|menu_action": "iframeDialog",
                # param_prefix + "jbmenu|track_menu_0|menu_icon": "dijitIconBookmark",
                # param_prefix + "jbmenu|track_menu_0|menu_label": "View transcript report",
                # param_prefix + "jbmenu|track_menu_0|menu_title": "Transcript {id}",
                # param_prefix + "jbmenu|track_menu_0|menu_url": "https://bipaa.genouest.org/some/link/to/features",  # TODO make this a param

                param_prefix + "jbstyle|max_height": "600",
                param_prefix + "jbstyle|style_classname": "transcript",
                param_prefix + "jbstyle|style_description": "note,description",
                param_prefix + "jbstyle|style_height": "10px",
                param_prefix + "jbstyle|style_label": "product,name,id",
                param_prefix + "match_part|match_part_select": "false",
                param_prefix + "override_apollo_drag": "False",
                param_prefix + "override_apollo_plugins": "False",
                param_prefix + "track_config|html_options|topLevelFeatures": "",
                param_prefix + "track_config|track_class": "NeatHTMLFeatures/View/Track/NeatFeatures",
                param_prefix + "track_visibility": "default_off",
            }
            tool_params.update(track_params)
            track_num += 1

        tracks_by_cat = {}
        for t in ass.tracks:
            if t.category not in tracks_by_cat:
                tracks_by_cat[t.category] = []
            tracks_by_cat[t.category].append(t)

        for cat in tracks_by_cat:
            group_num += 1
            params = add_tracks_in_category(cat, tracks_by_cat[cat], group_num)
            tool_params.update(params)

        # Add bigwig tracks for rnaseq
        tracks_by_cat_wig = {}
        for t in ass.tracks:
            if t.type == "rnaseq":
                wig_cat = "{}{}".format(t.category, ass.wig_category_suffix)
                if wig_cat not in tracks_by_cat_wig:
                    tracks_by_cat_wig[wig_cat] = []

                tracks_by_cat_wig[wig_cat].append(t)

        for cat in tracks_by_cat_wig:
            group_num += 1
            params = add_tracks_in_category(cat, tracks_by_cat_wig[cat], group_num, upload_prefix='track_wig', track_type="wig")
            tool_params.update(params)

        dest_rename = {
            'output': 'jbrowse.zip'
        }

        runner = bo.get_runner('galaxy', ass, task_id)
        exit_code, out, err = runner.run_or_resume_job(tool=tool, params=tool_params, uploads=file_uploads, dest_rename=dest_rename, check_output=False)

        exit_code_all += exit_code

        if (runner.task.has_run or not os.path.isfile(ass.get_derived_path('jbrowse'))) and exit_code_all == 0:
            if os.path.isfile(ass.get_derived_path('jbrowse')):
                os.remove(ass.get_derived_path('jbrowse'))

            log.info("Extracting data dir from downloaded archive + converting to tar.gz")
            with ZipFile(os.path.join(ass.get_work_dir(), "jbrowse/jbrowse.zip")) as zipf:

                # First find all fake files that we sent
                with zipf.open('data/trackList.json') as trl:
                    trl = json.load(trl)

                    to_swap = ass.jbrowse_track_swapping(trl['tracks'], ass.get_track_paths())

                    # Using the usable path here, but for production this will be replace on-the-fly by locked path while deploying
                    # (locked path may not be known here yet if using gopublish for example)
                    replace_fake_files(ass.get_derived_path('2bit'), ass.get_derived_path('jbrowse'), to_swap, zipf)

            # Output checking is delayed as we post process the result locally

            exit_code_all += runner.task.check_expected_outputs()

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
