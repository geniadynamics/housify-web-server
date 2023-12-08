import asyncio
import subprocess
import os


async def run_command(command):
    """Run a command asynchronously using subprocess."""
    process = await asyncio.create_subprocess_exec(
        *command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode and process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode, command, output=stdout, stderr=stderr
        )
    return stdout


async def generate_ecdsa_key_pair(key_dir):
    """Generate ECDSA key pair and store them in the specified directory."""
    try:
        os.makedirs(key_dir, exist_ok=True)
        private_key_path = os.path.join(key_dir, "ec_private.pem")
        public_key_path = os.path.join(key_dir, "ec_public.pem")

        await run_command(
            [
                "openssl",
                "ecparam",
                "-genkey",
                "-name",
                "secp521r1",
                "-noout",
                "-out",
                private_key_path,
            ]
        )

        await run_command(
            [
                "openssl",
                "ec",
                "-in",
                private_key_path,
                "-pubout",
                "-out",
                public_key_path,
            ]
        )

        print("ECDSA key pair generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


secure_key_directory = "../"

asyncio.run(generate_ecdsa_key_pair(secure_key_directory))
