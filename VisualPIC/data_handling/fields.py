# -*- coding: utf-8 -*-

#Copyright 2016-2018 Angel Ferran Pousa, DESY
#
#This file is part of VisualPIC.
#
#VisualPIC is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#VisualPIC is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with VisualPIC.  If not, see <http://www.gnu.org/licenses/>.


class Field():
    def __init__(self, field_name, field_timesteps, species_name=None):
        self.field_name = field_name
        self.field_timesteps = field_timesteps
        self.species_name = species_name

    def get_data(self, time_step, field_units=None, axes_units=None,
                 time_units=None, slice_i=0.5, slice_j=0.5, slice_dir_i=None,
                 slice_dir_j=None, m=0, theta=0):
        raise NotImplementedError

    def get_only_metadata(self, time_step):
        raise NotImplementedError


class FolderField(Field):
    def __init__(self, field_name, field_path, field_files, field_timesteps,
                 field_reader, unit_converter, species_name=None):
        super().__init__(field_name, field_timesteps, species_name)
        self.field_path = field_path
        self.field_files = field_files
        self.field_reader = field_reader
        self.unit_converter = unit_converter

    def get_data(self, time_step, field_units=None, axes_units=None,
                 axes_to_convert=None, time_units=None, slice_i=0.5,
                 slice_j=0.5, slice_dir_i=None, slice_dir_j=None, m=0,
                 theta=0):
        file_path = self._get_file_path(time_step)
        fld, fld_md = self.field_reader.read_field(
            file_path, self.field_path, slice_i, slice_j, slice_dir_i,
            slice_dir_j, m, theta)
        # perform unit conversion
        unit_list = [field_units, axes_units, time_units]
        if any(unit is not None for unit in unit_list):
            fld, fld_md  = self.unit_converter.convert_field_units(
                fld, fld_md, target_field_units=field_units,
                target_axes_units=axes_units, axes_to_convert=axes_to_convert,
                target_time_units=time_units)
        return fld, fld_md

    def get_only_metadata(self, time_step):
        file_path = self._get_file_path(time_step)
        return self.field_reader.read_field_metadata(
            file_path, self.field_path)

    def _get_file_path(self, time_step):
        ts_i = self.field_timesteps.tolist().index(time_step)
        return self.field_files[ts_i]