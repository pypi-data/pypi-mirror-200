# blockinfile

`blockinfile` is a tool for editing automatically a text block surrounded by marker lines. It's an automated port of ansible's [blockinfile module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/blockinfile_module.html).

## Usage

```
blockinfile --path FILE_TO_PATCH --block CONTENT_TO_INSERT [--marker NAME] [--marker-begin START_STRING] [--marker-end END_STRING] [MORE_OPTIONS]
```

Options are the same as in [Ansible documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/blockinfile_module.html).

## Sample

#### If `myfile.conf` initially contains:

```
sample line
other line
```

#### Then running:

```
blockinfile --path myfile.conf --marker "# {mark} MY BLOCK" --block 'this line will be entered
this one too'
```

Then myfile.conf will be updated:

```
sample line
other line
# BEGIN MY BLOCK
this line will be entered
this one too
# END MY BLOCK
```

#### Then running:

```
blockinfile --path myfile.conf --marker "# {mark} MY BLOCK" --block 'updating the section'
```

Would produce:

```
sample line
other line
# BEGIN MY BLOCK
updating the section
# END MY BLOCK
```

## "Automated" port

This project includes the source of Ansible's `blockinfile` module, slightly modified so it can work without having to use or even install Ansible. The modifications have been automated so it should be possible to easily port newer Ansible versions.

See [`builder/build.sh`](builder/build.sh).

## License

Since `blockinfile` is a port of (part of) Ansible's source, it's licensed under GPLv3+ just like Ansible.
