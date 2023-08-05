import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import (
    StratifiedShuffleSplit,
    StratifiedKFold,
    KFold,
    train_test_split,
)
from typing import Optional, Union, List, Tuple
from pathlib import Path
import copy


class DataFrame():
    def __init__(
        self, df: pd.DataFrame, random_state: int = 42, *args, **kargs
    ) -> None:
        super(DataFrame, self).__init__()
        self.df = df.copy(deep=True)  # get a copy of original dataframe
        self.random_state = random_state

    def __repr__(self) -> str:
        return repr(self.df)

    def split_df(
        self,
        val: bool = False,
        test_size: float = 0.1,
        val_size: Optional[float] = None,
    ):
        if val:
            assert val_size is not None, "val size needed"
            val_num, test_num = len(self.df) * [val_size, test_size]

            train_df, val_df = train_test_split(
                self.df, test_size=int(val_num), random_state=self.random_state
            )
            train_df, test_df = train_test_split(
                train_df, test_size=int(test_num), random_state=self.random_state
            )
            return train_df, val_df, test_df
        else:
            train_df, test_df = train_test_split(
                train_df, test_size=test_size, random_state=self.random_state
            )
            return train_df, test_df

    def stratified_split_df(
        self, labels: Union[List[str], str], n_splits: int = 1, test_size: float = 0.1
    ) -> Union[List, Tuple]:
        split = StratifiedShuffleSplit(
            n_splits=n_splits, test_size=test_size, random_state=self.random_state
        )
        df_trains = []
        df_tests = []
        for train_index, test_index in split.split(self.df, self.df[labels]):
            strat_train_set = self.df.loc[train_index]
            strat_test_set = self.df.loc[test_index]
            df_trains.append(strat_train_set)
            df_tests.append(strat_test_set)

        return (
            (strat_train_set, strat_test_set)
            if n_splits == 1
            else (df_trains, df_tests)
        )

    def stratified_kfold_split_df(
        self, labels: Union[List[str], str], n_splits: int = 2
    ) -> Tuple:
        assert n_splits >= 2, "At least 2 fold"
        skf = StratifiedKFold(
            n_splits=n_splits, shuffle=True, random_state=self.random_state
        )
        for train_index, test_index in skf.split(self.df, self.df[labels]):
            strat_train_set = self.df.loc[train_index]
            strat_test_set = self.df.loc[test_index]
            yield strat_train_set, strat_test_set

    def kfold_split_df(self, labels: Union[List[str], str], n_splits: int = 2) -> Tuple:
        assert n_splits >= 2, "At least 2 fold"
        df_trains = []
        df_tests = []
        skf = StratifiedKFold(
            n_splits=n_splits, shuffle=True, random_state=self.random_state
        )
        for train_index, test_index in skf.split(self.df, self.df[labels]):
            strat_train_set = self.df.loc[train_index]
            strat_test_set = self.df.loc[test_index]
            df_trains.append(strat_train_set)
            df_tests.append(strat_test_set)

        return df_trains, df_tests

    def show_ratio(self, label="label", sort=None, n: Optional[int] = None):
        """print the label proportion in pd.DataFrame
        Args:
            sort: 'value' or 'label'
        """
        n_all = len(self.df)
        if sort == "value":
            n_classes = (
                self.df[label]
                .value_counts()
                .reset_index()
                .sort_values(by=label, ascending=False)
            )
        elif sort == "label":
            n_classes = (
                self.df[label].value_counts().reset_index().sort_values(by="index")
            )
        else:
            n_classes = self.df[label].value_counts().reset_index()
        if n:
            n_classes = n_classes[:n]

        for i in n_classes.index:
            print(
                f'Label, {n_classes.at[i, "index"]} takes: {n_classes.at[i, label] / n_all * 100:.2f}%, Nums: {n_classes.at[i, label]}'
            )


def read_csv(path: str = "", random_state: int = 42, *args, **kargs):
    _path = Path(path)
    assert _path.is_file(), "not a file"
    return DataFrame(df=pd.read_csv(path, *args, **kargs), random_state=random_state)


def split_df(df: pd.DataFrame, shuf=True, val=True, random_state=42):
    """Split df into train/val/test set and write into files
    ratio: 8:1:1 or 9:1

    Args:
        - df (DataFrame): some data
        - shuf (bool, default=True): shuffle the DataFrame
        - val (bool, default=True): split into three set, train/val/test
    """
    if shuf:
        df = shuffle(df, random_state=random_state)

    sep = int(len(df) * 0.1)

    if val:
        test_df = df.iloc[:sep]
        val_df = df.iloc[sep : sep * 2]
        train_df = df.iloc[sep * 2 :]
        return train_df, val_df, test_df
    else:
        test_df = df.iloc[:sep]
        train_df = df.iloc[sep:]
        return train_df, test_df


def show_ratio(df: pd.DataFrame, label="label", sort=None, n=5) -> None:
    """print the label proportion in pd.DataFrame
    Args:
        sort: 'value' or 'label'
    """
    n_all = len(df)
    if sort == "value":
        n_classes = (
            df[label]
            .value_counts()
            .reset_index()
            .sort_values(by=label, ascending=False)
        )
    elif sort == "label":
        n_classes = df[label].value_counts().reset_index().sort_values(by="index")
    else:
        n_classes = df[label].value_counts().reset_index()

    n_classes = n_classes[:n]

    for i in n_classes.index:
        print(
            f'Label {n_classes.at[i, "index"]} takes: {n_classes.at[i, label] / n_all * 100:.2f}%, Nums: {n_classes.at[i, label]}'
        )
