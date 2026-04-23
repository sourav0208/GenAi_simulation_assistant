import os
from fastapi import HTTPException

def enforce_cloud_limits(config):

   
    if os.getenv("RENDER"):

        if config.solver == "pinn":

            max_epochs = 100
            max_hidden = 32

            if config.epochs and config.epochs > max_epochs:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Cloud demo limit exceeded. "
                        f"Max epochs allowed on cloud: {max_epochs}. "
                        f"For larger jobs, run locally."
                    )
                )

            if config.hidden_dim and config.hidden_dim > max_hidden:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Cloud demo limit exceeded. "
                        f"Max hidden_dim allowed on cloud: {max_hidden}. "
                        f"For larger jobs, run locally."
                    )
                )

    return config