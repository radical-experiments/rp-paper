#!/usr/bin/env python
"""This script does x.

Example:

Attributes:

Todo:

"""

import os
import sys
import glob
import numpy as np
import pandas as pd
import radical.analytics as ra


def initialize_entity(ename=None):
    entities = {'session': {'sid'          : [],     # Session ID
                            'session'      : [],     # RA session objects
                            'experiment'   : [],     # Experiment ID
                            'TTC'          : [],     # Time to completion
                            'nhost'        : [],     # #host for CU execution
                            'nunit'        : [],     # #units
                            'nunit_done'   : [],     # #active units
                            'nunit_failed' : [],     # #failed units
                            'npilot'       : [],     # #pilots
                            'npilot_active': [],     # #active pilots
                            'ncore'        : [],     # #cores
                            'ncore_active' : []},    # #active cores
                'pilot'  : {'pid'          : [],     # Pilot ID
                            'sid'          : [],     # Session ID
                            'hid'          : [],     # Host ID
                            'ncore'        : [],     # #cores
                            'nunit'        : [],     # #units executed
                            'experiment'   : []},    # Experiment ID
                'unit'   : {'uid'          : [],     # Unit ID
                            'sid'          : [],     # Session ID
                            'pid'          : [],     # Pilot ID
                            'hid'          : [],     # Host ID
                            'experiment'   : []}}    # Experiment ID

    # Add the duration label of each state of each entity.
    for duration in pdm.keys():
        entities['session'][duration] = []
        entities['pilot'][duration] = []
    for duration in udm.keys():
        entities['session'][duration] = []
        entities['unit'][duration] = []

    # Return the empty data structure of the requested entity.
    if ename in ['session', 'pilot', 'unit']:
        return entities[ename]
    else:
        error = 'Cannot itialize entity %s' % ename
        print error
        sys.exit(1)


def load_df(ename=None):
    if ename in ['session', 'pilot', 'unit']:
        df = pd.DataFrame(initialize_entity(ename=ename))
        if os.path.isfile(csvs[ename]):
            df = pd.read_csv(csvs[ename], index_col=0)
        return df
    else:
        error = 'Cannot itialize entity %s' % ename
        print error
        sys.exit(1)


def store_df(new_df, stored=pd.DataFrame(), ename=None):
    # skip storing if no new data are passed.
    if new_df.empty:
        print 'WARNING: attempting to store an empty DF.'
    else:
        if ename == 'session':
            new_sessions = new_df.drop('session', axis=1)
            if stored.empty:
                sessions = new_sessions
            else:
                sessions = stored.append(new_sessions)
            sessions.to_csv(csvs[ename])

        elif ename in ['pilot', 'unit']:
            if stored.empty:
                df = new_df
            else:
                df = stored.append(new_df)
            df.reset_index(inplace=True, drop=True)
            df.to_csv(csvs[ename])

        else:
            error = 'Cannot store DF to %s' % ename
            print error
            sys.exit(1)


def parse_osg_hostid(hostid):
    '''
    Heuristic: eliminate node-specific information from hostID.
    '''
    domain = None

    # Split domain name from IP.
    host = hostid.split(':')

    # Split domain name into words.
    words = host[0].split('.')

    # Get the words in the domain name that do not contain
    # numbers. Most hostnames have no number but there are
    # exceptions.
    literals = [l for l in words if not
                any((number in set('0123456789')) for number in l)]

    # Check for exceptions:
    # a. every word of the domain name has a number
    if len(literals) == 0:

        # Some hostname use '-' instead of '.' as word separator.
        # The parser would have returned a single word and the
        # any of that word may have a number.
        if '-' in host[0]:
            words = host[0].split('-')
            literals = [l for l in words if not
                        any((number in set('0123456789')) for number in l)]

            # FIXME: We do not check the size of literals.
            domain = '.'.join(literals)

        # Some hostnames may have only the name of the node. We
        # have to keep the IP to decide later on whether two nodes
        # are likely to belong to the same cluster.
        elif 'nod' in host[0]:
            domain = '.'.join(host)

        # FIXME: ad hoc parsing
        elif 'n0' in host[0]:
            domain = 'n0x.10.2.x.x'

        # The hostname is identified by an alphanumeric string
        else:
            domain = '.'.join(host)

    # Some hostnames DO have numbers in their name.
    elif len(literals) == 1:
        domain = '.'.join(words[1:])

    # Some hostname are just simple to parse.
    else:
        domain = '.'.join(literals)

    # FIXME: When everything else fails, ad hoc manipulations of
    #        domain string.
    if 'its.osg' in domain:
        domain = 'its.osg'
    elif 'nodo' in domain:
        domain = 'nodo'
    elif 'bu.edu' in domain:
        domain = 'bu.edu'

    return domain


def load_pilots(sid, exp, sra_pilots, pdm, pu_rels):
    sys.stdout.write('\n%s --- %s' % (exp, sid))
    ps = initialize_entity(ename='pilot')

    # Did we already store pilots of this session?
    stored_pilots = load_df(ename='pilot')
    stored_pids = []
    if stored_pilots['sid'].any():
        stored_pilots_sid = stored_pilots.loc[
            stored_pilots['sid'] == sid].copy()
        stored_pids = stored_pilots_sid['pid'].values.tolist()

    # Derive properties and duration for each pilot.
    for pid in sorted(sra_pilots.list('uid')):

        # Skip session if its pilots have been already stored.
        if pid in stored_pids:
            sys.stdout.write('\n%s already in %s' % (pid, csvs['pilot']))
            continue

        # Pilot properties.
        sys.stdout.write('\n' + pid + ': ')
        ps['pid'].append(pid)
        ps['sid'].append(sid)
        ps['experiment'].append(exp)

        # Host ID.
        pentity = sra_pilots.get(uid=pid)[0]
        if pentity.cfg['hostid']:
            ps['hid'].append(parse_osg_hostid(pentity.cfg['hostid']))
        else:
            ps['hid'].append(None)

        # Number of cores of the pilot.
        ps['ncore'].append(pentity.description['cores'])

        # Number of units executed.
        ps['nunit'].append(len(pu_rels[pid]))

        # Pilot durations.
        for duration in pdm.keys():
            if duration not in ps.keys():
                ps[duration] = []
            try:
                ps[duration].append(pentity.duration(pdm[duration]))
                sys.stdout.write(' %s' % duration)
            except:
                print '\nWARNING: Failed to calculate duration %s' % \
                    duration
                ps[duration].append(None)

    # Store pilots DF to csv and reload into memory to return the complete
    # DF for the given sid.
    if ps['pid']:
        pilots = pd.DataFrame(ps)
        store_df(pilots, stored=stored_pilots, ename='pilot')
        stored_pilots = load_df(ename='pilot')
        print '\nstored in %s.' % csvs['pilot']

    # Returns the DF of the stored pilots if no new pilots have been added;
    # the DF with the old and new pilots otherwise.
    return stored_pilots


def load_units(sid, exp, sra_units, udm, pilots, sra, pu_rels):

    sys.stdout.write('\n%s --- %s' % (exp, sid))
    us = initialize_entity(ename='unit')

    # Did we already store units of this session?
    stored_units = load_df(ename='unit')
    stored_uids = []
    if stored_units['sid'].any():
        stored_units_sid = stored_units.loc[
            stored_units['sid'] == sid].copy()
        stored_uids = stored_units_sid['uid'].values.tolist()

    # Derive properties and duration for each unit.
    for uid in sorted(sra_units.list('uid')):

        # Skip session if its pilots have been already stored.
        if uid in stored_uids:
            sys.stdout.write('\n%s already stored in %s' %
                             (uid, csvs['unit']))
            continue

        # Properties.
        sys.stdout.write('\n' + uid + ': ')
        us['uid'].append(uid)
        us['sid'].append(sid)
        us['experiment'].append(exp)

        # Durations.
        uentity = sra_units.get(uid=uid)[0]
        for duration in udm.keys():
            if duration not in us.keys():
                us[duration] = []
            try:
                # TODO: this is a temporary fix for inconsistent state model.
                if duration == 'U_AGENT_EXECUTING':
                    if 'AGENT_STAGING_OUTPUT_PENDING' in \
                            uentity.states.keys() and \
                       'FAILED' in uentity.states.keys():
                            us[duration].append(None)
                            continue
                us[duration].append(uentity.duration(udm[duration]))
                sys.stdout.write(' %s' % duration)
            except:
                print '\nWARNING: Failed to calculate duration %s' % \
                    duration
                us[duration].append(None)

        # pilot and host on which the unit has been executed.
        punit = [key[0] for key in pu_rels.items() if uid in key[1]][0]
        hid = pilots[(pilots['sid'] == sid) &
                     (pilots['pid'] == punit)]['hid'].tolist()[0]
        us['pid'].append(punit)
        us['hid'].append(hid)

    # Store unit DF to csv and reload into memory to return the complete
    # DF for the given sid.
    if us['pid']:
        units = pd.DataFrame(us)
        store_df(units, stored=stored_units, ename='unit')
        stored_units = load_df(ename='unit')
        print '\nstored in %s.' % csvs['unit']

    # Returns the DF of the stored pilots if no new pilots have been added;
    # the DF with the old and new pilots otherwise.
    return stored_units


def load_session(sid, exp, sra_session, sra_pilots, sra_units,
                 pdm, udm, pilots, units):

    # IF this session has been already stored get out, nothing to do here.
    stored_sessions = load_df(ename='session')
    if sid in stored_sessions.index.tolist():
        sys.stdout.write('%s already stored in %s' % (sid, csvs['session']))
        return False

    sys.stdout.write('\n%s --- %s' % (exp, sid))
    s = initialize_entity(ename='session')

    # Session properties: pilots and units.
    # sp = sra_session.filter(etype='pilot', inplace=False)
    # su = sra_session.filter(etype='unit', inplace=False)
    s['sid'].append(sid)
    s['session'].append(None)
    s['experiment'].append(exp)
    s['TTC'].append(sra_session.ttc)
    s['nhost'].append(len(pilots.loc[pilots['sid'] == sid]['hid'].unique()))
    s['nunit'].append(len(sra_units.get()))
    s['npilot'].append(len(sra_pilots.get()))
    s['npilot_active'].append(len(sra_pilots.timestamps(state='PMGR_ACTIVE')))
    s['ncore'].append(pilots[pilots.sid == sid].ncore.sum())
    s['ncore_active'].append(pilots[(pilots.sid == sid) & (pilots.P_LRMS_RUNNING > 0)].ncore.sum())
    s['nunit_done'].append(len(sra_units.timestamps(state='DONE')))
    s['nunit_failed'].append(len(sra_units.timestamps(state='FAILED')))

    # Pilots total durations.  NOTE: s initialization guarantees
    # the existence of duration keys.
    for duration in pdm.keys():
        s[duration].append(sra_pilots.duration(pdm[duration]))

    # Units total durations. NOTE: s initialization guarantees the
    # existence of duration keys.
    for duration in udm.keys():
        s[duration].append(sra_units.duration(udm[duration]))

    # Store session.
    session = pd.DataFrame(s, index=[sid])
    store_df(session, stored=stored_sessions, ename='session')
    print '\nstored in %s' % csvs['session']

    return True


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    datadir = '../data/'
    experiment_tag = 'exp'

    # Global constants
    # File names where to save the DF of each entity of each session.
    csvs = {'session': '%ssessions.csv' % datadir,
            'pilot'  : '%spilots.csv' % datadir,
            'unit'   : '%sunits.csv' % datadir}

    # Model of pilot durations.
    pdm = {'P_PMGR_SCHEDULING': ['NEW',
                                 'PMGR_LAUNCHING_PENDING'],
           'P_PMGR_QUEUING'   : ['PMGR_LAUNCHING_PENDING',
                                 'PMGR_LAUNCHING'],
           'P_LRMS_SUBMITTING': ['PMGR_LAUNCHING',
                                 'PMGR_ACTIVE_PENDING'],
           'P_LRMS_QUEUING'   : ['PMGR_ACTIVE_PENDING',
                                 'PMGR_ACTIVE'],
           'P_LRMS_RUNNING'   : ['PMGR_ACTIVE',
                                 ['DONE', 'CANCELED', 'FAILED']]}

    # Model of unit durations.
    udm = {'U_UMGR_SCHEDULING'   : ['NEW',
                                    'UMGR_SCHEDULING_PENDING'],
           'U_UMGR_BINDING'      : ['UMGR_SCHEDULING_PENDING',
                                    'UMGR_SCHEDULING'],
           #    'I_UMGR_SCHEDULING'   : ['UMGR_SCHEDULING',
           #                             'UMGR_STAGING_INPUT_PENDING'],
           #    'I_UMGR_QUEING'       : ['UMGR_STAGING_INPUT_PENDING',
           #                             'UMGR_STAGING_INPUT'],
           #    'I_AGENT_SCHEDULING'  : ['UMGR_STAGING_INPUT',
           #                             'AGENT_STAGING_INPUT_PENDING'],
           #    'I_AGENT_QUEUING'     : ['AGENT_STAGING_INPUT_PENDING',
           #                             'AGENT_STAGING_INPUT'],
           #    'I_AGENT_TRANSFERRING': ['AGENT_STAGING_INPUT',
           #                             'AGENT_SCHEDULING_PENDING'],
           'U_AGENT_QUEUING'     : ['AGENT_SCHEDULING_PENDING',
                                    'AGENT_SCHEDULING'],
           'U_AGENT_SCHEDULING'  : ['AGENT_SCHEDULING',
                                    'AGENT_EXECUTING_PENDING'],
           'U_AGENT_QUEUING_EXEC': ['AGENT_EXECUTING_PENDING',
                                    'AGENT_EXECUTING'],
           'U_AGENT_EXECUTING'   : ['AGENT_EXECUTING',
                                    'AGENT_STAGING_OUTPUT_PENDING']}
    #    'O_AGENT_QUEUING'     : ['AGENT_STAGING_OUTPUT_PENDING',
    #                             'AGENT_STAGING_OUTPUT'],
    #    'O_UMGR_SCHEDULING'   : ['AGENT_STAGING_OUTPUT',
    #                             'UMGR_STAGING_OUTPUT_PENDING'],
    #    'O_UMGR_QUEUING'      : ['UMGR_STAGING_OUTPUT_PENDING',
    #                             'UMGR_STAGING_OUTPUT'],
    #    'O_UMGR_TRANSFERRING' : ['UMGR_STAGING_OUTPUT',
    #                             ['DONE', 'CANCELED', 'FAILED']]}

    # Get sessions ID, experiment number and RA object. Assume:
    # datadir/exp*/sessiondir/session.json.
    for path in glob.glob('%s/%s*' % (datadir, experiment_tag)):
        for sdir in glob.glob('%s/*' % path):

            # Session ID and session experiment.
            sid = glob.glob('%s/*.json' % sdir)[0].split('/')[-1:][0][:-5]
            exp = path.split('/')[-1:][0]

            # Consistency check: SID of json file name is the same SID of
            # directory name.
            if sid == sdir.split('/')[-1:][0]:

                # RA objects cannot be serialize: every RA session object need
                # to be constructed at every run.
                sra_session = ra.Session(sid, 'radical.pilot', src=sdir)

                # Pilot-unit relationship dictionary
                pu_rels = sra_session.describe('relations', ['pilot', 'unit'])

                # Pilots of sra: dervie properties and durations.
                print '\n\n%s -- %s -- Loading pilots:' % (exp, sid)
                sra_pilots = sra_session.filter(etype='pilot', inplace=False)
                pilots = load_pilots(sid, exp, sra_pilots, pdm, pu_rels)

                # Units of sra: dervie properties and durations.
                print '\n\n%s -- %s -- Loading units:' % (exp, sid)
                sra_units = sra_session.filter(etype='unit', inplace=False)
                units = load_units(sid, exp, sra_units, udm, pilots,
                                   sra_session, pu_rels)

                # Session of sra: derive properties and total durations.
                print '\n\n%s -- %s -- Loading session:\n' % (exp, sid)
                load_session(sid, exp, sra_session, sra_pilots, sra_units,
                             pdm, udm, pilots, units)

            else:
                error = 'ERROR: session folder and json file name differ'
                print '%s: %s != %s' % (error, sdir, sid)
