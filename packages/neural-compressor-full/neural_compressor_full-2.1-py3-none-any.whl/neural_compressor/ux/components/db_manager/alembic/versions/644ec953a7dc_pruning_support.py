# -*- coding: utf-8 -*-
# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# flake8: noqa
# mypy: ignore-errors
"""pruning_support

Revision ID: 644ec953a7dc
Revises: 6ece06672ed3
Create Date: 2022-12-09 17:22:17.310141

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import sessionmaker

from neural_compressor.ux.components.db_manager.db_manager import DBManager
from neural_compressor.ux.components.db_manager.db_models.optimization_type import OptimizationType
from neural_compressor.ux.components.db_manager.db_models.precision import (
    Precision,
    precision_optimization_type_association,
)
from neural_compressor.ux.utils.consts import OptimizationTypes, Precisions

db_manager = DBManager()
Session = sessionmaker(bind=db_manager.engine)

# revision identifiers, used by Alembic.
revision = "644ec953a7dc"
down_revision = "6ece06672ed3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with Session.begin() as db_session:
        pruning_optimization_id = OptimizationType.add(
            db_session=db_session,
            name=OptimizationTypes.PRUNING.value,
        )
        fp32_precision_id = Precision.get_precision_by_name(
            db_session=db_session,
            precision_name=Precisions.FP32.value,
        )[0]

        query = precision_optimization_type_association.insert().values(
            precision_id=fp32_precision_id,
            optimization_type_id=pruning_optimization_id,
        )
        db_session.execute(query)

    op.create_table(
        "pruning_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("train", sa.String(), nullable=True),
        sa.Column("approach", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("modified_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pruning_details")),
    )
    with op.batch_alter_table("pruning_details", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_pruning_details_id"), ["id"], unique=True)

    op.create_table(
        "example",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("framework", sa.Integer(), nullable=False),
        sa.Column("domain", sa.Integer(), nullable=False),
        sa.Column("dataset_type", sa.String(length=50), nullable=False),
        sa.Column("model_url", sa.String(length=250), nullable=False),
        sa.Column("config_url", sa.String(length=250), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["domain"], ["domain.id"], name=op.f("fk_example_domain_domain")),
        sa.ForeignKeyConstraint(
            ["framework"], ["framework.id"], name=op.f("fk_example_framework_framework")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_example")),
    )
    with op.batch_alter_table("example", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_example_id"), ["id"], unique=False)

    with op.batch_alter_table("model", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "supports_pruning",
                sa.Boolean(),
                default=False,
                nullable=True,
            ),
        )
    op.execute("UPDATE model SET supports_pruning = false")

    with op.batch_alter_table("model", schema=None) as batch_op:
        batch_op.alter_column("supports_pruning", nullable=False)

    with op.batch_alter_table("optimization", schema=None) as batch_op:
        batch_op.add_column(sa.Column("pruning_details_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f("fk_optimization_pruning_details_id_pruning_details"),
            "pruning_details",
            ["pruning_details_id"],
            ["id"],
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("optimization", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_optimization_pruning_details_id_pruning_details"), type_="foreignkey"
        )
        batch_op.drop_column("pruning_details_id")

    with op.batch_alter_table("model", schema=None) as batch_op:
        batch_op.drop_column("supports_pruning")

    with op.batch_alter_table("example", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_example_id"))

    op.drop_table("example")
    with op.batch_alter_table("pruning_details", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_pruning_details_id"))

    op.drop_table("pruning_details")
    # ### end Alembic commands ###
