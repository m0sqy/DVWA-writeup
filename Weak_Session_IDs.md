# Weak Session IDs

Objective

This module uses four different ways to set the dvwaSession cookie value, the
objective of each level is to work out how the ID is generated and then infer
the IDs of other system users.

## low

Session id is incremented by 1 at each time with initial value 0.

## medium

Session id is the current UNIX timestamp.

## high

Session id is just the one in low security, but as a MD5 hex digest.
