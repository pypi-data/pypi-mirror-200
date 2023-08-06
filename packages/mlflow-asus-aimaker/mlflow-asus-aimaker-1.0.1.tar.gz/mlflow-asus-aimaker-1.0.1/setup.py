from setuptools import setup, find_packages

setup(
    name="mlflow-asus-aimaker",
    version="1.0.1",
    description="MLflow plugin for ASUS AI-Maker",
    packages=find_packages(),
    install_requires=["AIMaker", "protobuf==3.20.1", "numpy<1.24", "mlflow==1.24.0"],
    entry_points={
        "mlflow.tracking_store": "file-plugin=mlflow_plugin.plugin_rest_store:PluginRestStore",
        "mlflow.model_registry_store": "file-plugin=mlflow_plugin.plugin_model_rest_store:PluginRegistryRestStore"
    },
)
