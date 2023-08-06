.. -*- coding: utf-8 -*-
.. :Project:   SoL
.. :Created:   mar 04 feb 2014 09:07:53 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2014, 2020 Lele Gaifax
..

.. _competitors fixup:

Competitors fixup
=================

.. index::
   pair: Competitors fixup; Tourneys

It was seen already, it will happen again: somebody gave you the wrong name, or you
misunderstood or whatever, but now you have a tourney with the wrong player and you need to
manually tweak the list of competitors.

.. important:: You may fix the problem at any time, even after the price-giving. However be
               sure to do that **before** sharing the tourney's data with another instance of
               SoL, otherwise the same manual fix shall be repeated on the other side(s) as
               well.

The :ref:`tourneys <tourneys management>` window offers a :guilabel:`Competitors` button that
will show the usual grid window with the competitors of that particular tourney. You cannot
insert or delete players from here (use the :ref:`competitors panel` functionalities for that),
you can just replace any player with any other one.

.. warning:: Little to none verifications are done, so you better be sure of what you are
             doing, checking twice before confirming the changes. For example, the combos let
             you insert the *same* player twice, that won't be accepted by the database and
             will cause an error.

.. _competitors position:

Position
--------

In special cases, in particular in :ref:`knockout tournaments <knockout system>`, you may want
to explicitly set the :guilabel:`position` of each competitor: it will be used to determine the
initial ranking that in turn influences the generation of the first round.

The values are *arbitrary*, and they are relative, not absolute: competitors will be sorted
accordingly, in ascending order.

If inserted, the positions have priority over the *rating* of the competitors.
