# coding=utf-8

from __future__ import print_function, unicode_literals

import argparse
from collections import OrderedDict
from datetime import datetime, timedelta

from dateutil.parser import parse

from unicode_csv import UnicodeReader, UnicodeWriter


class Todo(object):

    @staticmethod
    def from_fields(fields):
        that = Todo()
        that.task = fields[0]
        that.folder = fields[1]
        that.context = fields[2]
        that.goal = fields[3]
        that.location = fields[4]
        that.start_date = parse(fields[5])
        that.start_time = parse(fields[6])
        that.due_date = parse(fields[7])
        that.duet_ime = parse(fields[8])
        that.repeat = fields[9]
        that.length = int(fields[10]) if fields[10] else None
        that.timer = int(fields[11]) if fields[11] else None
        that.priority = fields[12]
        that.tag = fields[13]
        that.status = fields[14]
        that.star = fields[15]
        that.note = fields[16]
        that.completed = parse(fields[17])
        return that


def get_todos_from_reader(reader):
    todos = []
    for i, fields in enumerate(reader):
        if i == 0:
            continue
        todo = Todo.from_fields(fields)
        todos.append(todo)
    return sorted(todos,key=lambda x: x.completed)


def get_latest_todos(todos, days=7):
    today_end = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return [x for x in todos if today_end - x.completed <= timedelta(days=days)]


def group_by_value(todos, value_name, value_list):
    if len(todos) == 0:
        return []
    last_todo = todos[0]
    value_dict = OrderedDict()
    for value in value_list:
        value_dict[value] = 0
    csv_res = [[None, value_dict]]
    for todo in todos:
        if todo.completed - last_todo.completed == timedelta(0):
            row = csv_res[-1]
            row[0] = datetime.strftime(todo.completed, '%Y-%m-%d')
        else:
            value_dict = OrderedDict()
            for value in value_list:
                value_dict[value] = 0
            row = [datetime.strftime(todo.completed, '%Y-%m-%d'), value_dict]
            csv_res.append(row)
        row[1][getattr(todo, value_name)] += todo.timer or 0
        last_todo = todo
    return csv_res


def write_group_by_one_filed(todos, output_path, value_name, values_list):
    csv_file = open(output_path, 'wb')
    res = group_by_value(todos, value_name, values_list)
    print('write: %s' % output_path)
    writer = UnicodeWriter(csv_file)

    row = ['complete']
    row.extend(values_list)
    writer.writerow(row)

    for row in res:
        output_row = [row[0]]
        for _, v in row[1].items():
            output_row.append(str(v))
        writer.writerow(output_row)


def write_timer(todos, output_path):
    csv_file = open(output_path, 'wb')
    date_timer = {}
    print('write: %s' % output_path)
    writer = UnicodeWriter(csv_file)

    for todo in todos:
        if not isinstance(todo.timer, int):
            continue
        if todo.completed not in date_timer:
            date_timer[todo.completed] = 0
        date_timer[todo.completed] += todo.timer

    row = ['date', 'timer']
    writer.writerow(row)

    for date, minutes in date_timer.items():
        output_row = [date.strftime('%Y-%m-%d'), "{0:.2f}".format(minutes / 60.0)]
        writer.writerow(output_row)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--days', type=int, default=7)
    arg_parser.add_argument('path')
    args = arg_parser.parse_args()

    todo_csv_str = open(args.path, 'rb')
    reader = UnicodeReader(todo_csv_str)
    todos = get_todos_from_reader(reader)
    latest_todos = get_latest_todos(todos, days=args.days)
    folders = list(set([x.folder for x in todos]))
    contexts = list(set([x.context for x in todos]))
    goals = list(set([x.goal for x in todos]))

    write_group_by_one_filed(latest_todos, args.path + '_group_by_folder.csv', 'folder', folders)
    write_group_by_one_filed(latest_todos, args.path + '_group_by_context.csv', 'context', contexts)
    write_group_by_one_filed(latest_todos, args.path + '_group_by_goal.csv', 'goal', goals)

    write_timer(latest_todos, args.path + '_timer.csv')


if __name__ == '__main__':
    main()
