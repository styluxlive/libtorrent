#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys

# to use this script, first run 'sample' to sample your libtorrent based process
# the output can then be passed to this script to auto-fold call stacks at
# relevant depths and to filter out low sample counts
f = open(sys.argv[1])


def parse_line(line):
    indentation = 0
    while indentation < len(line) and line[indentation] == ' ':
        indentation += 1
    if indentation == 0:
        return (0, 0, '')

    line = line.strip().split(' ')
    samples = int(line[0])
    fun = ' '.join(line[1:])

    return (indentation, samples, fun)


fold = -1

try:
    sample_limit = int(sys.argv[2])
except Exception:
    sample_limit = 5

fun_samples = {}

for line in f:
    if 'Sort by top of stack' in line:
        break

    indentation, samples, fun = parse_line(line)
    if samples < sample_limit:
        continue
    if fold != -1 and indentation > fold:
        continue
    fold = -1

    if '__gnu_cxx::__normal_iterator<' in fun:
        fold = indentation - 1
        continue

    if 'boost::_bi::bind_t' in fun:
        continue
    if 'boost::_bi::list' in fun:
        continue
    if 'boost::_mfi::mf' in fun:
        continue
    if 'boost::_bi::storage' in fun:
        continue

# should only add leaves
    if fun in fun_samples:
        fun_samples[fun] += samples
    else:
        fun_samples[fun] = samples

    output = '%s%-4d %s' % (' ' * (indentation / 2), samples, fun)
    if len(output) > 200:
        output = output[:200]
    print(output)

    if 'invariant_checker_impl' in fun:
        fold = indentation
    if 'free_multiple_buffers' in fun:
        fold = indentation
    if 'libtorrent::condition::wait' in fun:
        fold = indentation
    if 'allocate_buffer' in fun:
        fold = indentation
    if '::find_POD' in fun:
        fold = indentation
    if 'SHA1_Update' in fun:
        fold = indentation
    if 'boost::detail::function::basic_vtable' in fun:
        fold = indentation
    if 'operator new' in fun:
        fold = indentation
    if fun == 'malloc':
        fold = indentation
    if fun == 'free':
        fold = indentation
    if 'std::_Rb_tree' in fun:
        fold = indentation
    if 'pthread_cond_wait' in fun:
        fold = indentation
    if fun == 'mp_exptmod':
        fold = indentation
    if '::check_invariant()' in fun:
        fold = indentation
    if 'libtorrent::condition::wait' in fun:
        fold = indentation
    if '_sigtramp' in fun:
        fold = indentation
    if 'time_now_hires' in fun:
        fold = indentation
    if 'libtorrent::sleep' in fun:
        fold = indentation
    if fun == 'puts':
        fold = indentation
    if 'boost::asio::basic_stream_socket' in fun:
        fold = indentation
    if fun == 'recvmsg':
        fold = indentation
    if fun == 'sendmsg':
        fold = indentation
    if fun == 'semaphore_signal_trap':
        fold = indentation
    if 'boost::detail::atomic_count::operator' in fun:
        fold = indentation
    if fun == 'pthread_mutex_lock':
        fold = indentation
    if fun == 'pthread_mutex_unlock':
        fold = indentation
    if fun == '>::~vector()':
        fold = indentation
    if fun == 'szone_free_definite_size':
        fold = indentation
    if fun == 'snprintf':
        fold = indentation
    if fun == 'usleep':
        fold = indentation
    if fun == 'pthread_mutex_lock':
        fold = indentation
    if fun == 'pthread_mutex_unlock':
        fold = indentation
    if 'std::string::append' in fun:
        fold = indentation
    if fun == 'getipnodebyname':
        fold = indentation
    if '__gnu_debug::_Safe_iterator<std::' in fun:
        fold = indentation
    if fun == 'fflush':
        fold = indentation
    if fun == 'vfprintf':
        fold = indentation
    if fun == 'fprintf':
        fold = indentation
    if fun == 'BN_mod_exp':
        fold = indentation
    if fun == 'BN_CTX_free':
        fold = indentation
    if fun == 'cerror':
        fold = indentation
    if fun == '0xffffffff':
        fold = indentation

list = [(v, k) for k, v in fun_samples.items()]
list = sorted(list, reverse=True)

for i in list:
    print('%-4d %s' % (i[0], i[1]))
