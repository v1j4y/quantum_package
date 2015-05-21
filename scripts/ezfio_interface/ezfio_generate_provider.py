#!/usr/bin/env python

__author__ = "Applencourt PEP8"
__date__ = "jeudi 26 mars 2015, 12:49:35 (UTC+0100)"

"""
Creates the provider of a variable that has to be
fetched from the EZFIO file.
"""

import sys


class EZFIO_Provider(object):

    data = """
BEGIN_PROVIDER [ %(type)s, %(name)s %(size)s ]
  implicit none
  BEGIN_DOC
! %(doc)s
  END_DOC

  logical                        :: has
  PROVIDE ezfio_filename
  call ezfio_has_%(ezfio_dir)s_%(ezfio_name)s(has)
  if (has) then
    call ezfio_get_%(ezfio_dir)s_%(ezfio_name)s(%(name)s)
  else
    print *, '%(ezfio_dir)s/%(ezfio_name)s not found in EZFIO file'
    stop 1
  endif
%(write)s
END_PROVIDER
""".strip()

    write_correspondance = {"integer": "write_int",
                            "logical": "write_bool",
                            "double precision": "write_double"}

    def __init__(self):
        self.values = "type doc name ezfio_dir ezfio_name write output".split()
        for v in self.values:
            exec "self.{0} = None".format(v)

    def __repr__(self):
        self.set_write()
        for v in self.values:
            if not v:
                msg = "Error : %s is not set in EZFIO.cfg" % (v)
                print >>sys.stderr, msg
                sys.exit(1)
        if "size" not in self.__dict__:
            self.__dict__["size"] = ""

        return self.data % self.__dict__

    def set_write(self):
        self.write = ""
        if self.type in self.write_correspondance:
            write = self.write_correspondance[self.type]
            output = self.output
            name = self.name

            l_write = ["",
                       "  call write_time(%(output)s)",
                       "  call %(write)s(%(output)s, %(name)s, &",
                       "     '%(name)s')",
                       ""]

            self.write = "\n".join(l_write) % locals()

    def set_type(self, t):
        self.type = t.lower()

    def set_doc(self, t):
        self.doc = t.strip().replace('\n', '\n! ')

    def set_name(self, t):
        self.name = t

    def set_ezfio_dir(self, t):
        self.ezfio_dir = t.lower()

    def set_ezfio_name(self, t):
        self.ezfio_name = t.lower()

    def set_output(self, t):
        self.output = t

    def set_size(self, t):

        if t != "1":
            self.size = ", " + t
        else:
            self.size = ""

def test_module():
    T = EZFIO_Provider()
    T.set_type("double precision")
    T.set_name("thresh_SCF")
    T.set_doc("Threshold on the convergence of the Hartree Fock energy")
    T.set_ezfio_dir("Hartree_Fock")
    T.set_ezfio_name("thresh_SCF")
    T.set_output("output_Hartree_Fock")
    print T

if __name__ == '__main__':
    test_module()
